def bar(data):
    data_df = data[['product_id', 'ratingMean']].sort_values(by='product_id')
    data_df['v'] = data_df.groupby('product_id')['ratingMean'].transform(lambda x: x.count()).values
    heat_item = data_df[['product_id', 'v']].drop_duplicates()
    heat_item = heat_item.reset_index(drop=True)
    heat_item['R'] = data_df['ratingMean'].groupby(data_df['product_id']).mean().values
    heat_item['m'] = heat_item['v'].min()
    heat_item['C'] = data_df['ratingMean'].mean()
    heat_item['WR'] = heat_item.apply(lambda x: (x['v'] * x['R'] + x['m'] * x['C']) / (x['v'] + x['m']), axis=1)
    top_heat_item = heat_item.sort_values(by='WR', axis=0, ascending=False)
    top_heat_item = top_heat_item.reset_index(drop=True)
    top_heat_item['rank'] = top_heat_item.index + 1
    top_heat_item = top_heat_item.sort_values(by='product_id', axis=0)
    top_heat_item = top_heat_item.sort_values(by='rank', axis=0)
    top_heat_item = top_heat_item.reset_index(drop=True)
    return top_heat_item[['product_id', 'rank']]
