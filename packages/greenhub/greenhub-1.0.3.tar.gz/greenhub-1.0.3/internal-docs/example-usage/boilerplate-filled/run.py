import greenhub as gh
import pandas as pd
import pickle


def run(year: int, month: int):
    
    # Set  run parameters
    country = 'AR'
    state = 'SANTA FE'
    spatial_resolution = 'state'
    
    # Initialize GreenHub SDK (note that this step will be removed as soon as in production)
    gh.initialize("-")
    
    # Create feature vector
    features = create_feature_vector(country, year, spatial_resolution, state)

    # Load model
    with open('linear_regression.pkl', 'rb') as f:
        model = pickle.load(f)

    # Run model
    prediction = model.predict(features)

    # Format to expected GreenHub output
    output_dict = {'state': [state], 'prediction': prediction.tolist()}
    output = pd.DataFrame(output_dict)

    # Return model prediction
    return output


def create_feature_vector(country, start_year, spatial_resolution, state):

    # Prepare VI data
    vi = gh.get_vi_data(country=country, start_year=start_year, spatial_resolution=spatial_resolution)
    vi = vi[['EVI', 'NDVI', 'State', 'Year', 'Month']]
    vi['Year'] = pd.to_numeric(vi['Year'])
    vi = vi[vi['State'] == state]

    # Prepare soil data
    soil = gh.get_soil_data(country=country, spatial_resolution=spatial_resolution, layer='D1')
    selected_cols = [col for col in soil.columns if
                     (col.endswith('_avg') and not col.startswith('TP-')) or col in ['Layer', 'NAME_1']]
    soil = soil[selected_cols]
    soil.columns = soil.columns.str.replace('_avg', '')
    soil.rename({'NAME_1': 'State'}, axis=1, inplace=True)
    soil['State'] = soil['State'].apply(lambda x: x.upper())
    
    # Prepare climate data
    climate = gh.get_climate_data(country='AR', start_year=2010, end_year=2023, spatial_resolution='state')
    climate = climate.drop(columns=['CountryCode'])
    climate['Year'] = pd.to_numeric(climate['Year'])
    
    # Merge data
    merged_df = pd.merge(vi, soil, on='State', how='left')
    merged_df = pd.merge(merged_df, climate, on=['Year', 'Month', 'State'], how='left')
    merged_df = merged_df.dropna()

    # Create a pivot table
    pivot_df = merged_df.pivot_table(index=['Year', 'State'], columns='Month', aggfunc='first')

    # Flatten the MultiIndex columns
    pivot_df.columns = ['{}_Month{}'.format(col[0], int(col[1])) for col in pivot_df.columns]

    # Reset index to turn MultiIndex into columns
    pivot_df.reset_index(inplace=True)

    # Fix 12x columns for static values
    squash_cols = ['Drain', 'CFRAG', 'SDTO', 'STPC', 'CLPC', 'BULK', 'TAWC', 'CECS', 'BSAT', 'ESP',
                   'CECc', 'PHAQ', 'TCEQ', 'GYPS', 'ELCO', 'ORGC', 'TOTN', 'CNrt', 'ECEC', 'ALSA', 'Value']
    pivot_df = pivot_df.rename({f'{squash}_Month1': f'{squash}' for squash in squash_cols}, axis=1)
    pivot_df = pivot_df.drop(
        columns=[col for col in pivot_df.columns if any(col.startswith(f'{squash}_Month') for squash in squash_cols)])

    # Limit the feature vector to state
    single_state_df = pivot_df[pivot_df['State'] == state.upper()]
    single_state_df.head()

    # Final feature vector
    feature_vector = single_state_df.drop(columns=['Year', 'State'])
    feature_vector = feature_vector.dropna()

    return feature_vector
