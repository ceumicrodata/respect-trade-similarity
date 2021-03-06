import os
import pandas as pd
import json

THETA = 8.0

YEARS = ['{}'.format(y) for y in range(2001, 2018)]

NEW_MEMBER_STATES = 'CZ HU PL SI SK LV LT HR BG RO'.split()
CANDIDATE_COUNTRIES = 'AL BA TR MK ME RS'.split()
NEIGHBORHOOD_COUNTRIES = 'DZ MA TN AM AZ GE MD UA'.split()
PARTNERS = 'RU CN US'.split() + CANDIDATE_COUNTRIES + NEIGHBORHOOD_COUNTRIES

country_codes = pd.read_csv("input/iso-3166/countries.csv")
export_data = pd.read_csv('output/TC_INDEX_EXP_.csv',index_col=0)
import_data = pd.read_csv('output/TC_INDEX_IMP_.csv',index_col=0)

i = 0

str_list = ["EXP","IMP"]

for data_source in [export_data, import_data]:

  data_source = data_source.merge(country_codes, how='left', left_on='DECLARANT', right_on='iso3166_2').rename(columns={'country_name': 'declarant_name'})
  data_source = data_source.merge(country_codes, how='left', left_on='PARTNER', right_on='iso3166_2').rename(columns={'country_name': 'partner_name'})
  data_source = data_source[data_source.PARTNER.isin(PARTNERS)]

  def get_first_or_none(lst):
    return lst[0] if len(lst) else None

  def convert_index(KLD):
      return pd.np.exp(-1/THETA * KLD)

  def sort_data(Z):
      z = Z.values
      Z['sort'] = z.mean(axis=1)
      Z = Z.sort_values(by='sort', ascending=True).drop(columns='sort')
      return Z

  def prepare_data(data, year):
      Z = sort_data(
        convert_index(
          data.pivot(
            index='declarant_name', 
            columns='partner_name', 
            values='TCI_{}'
            .format(year)
            )
          )
        )

      z = Z.values.tolist()
      x = Z.columns.values.tolist()
      y = Z.index.values.tolist()
      return (x, y, z)

  def update_slopechart(Partner):
      Declarants, Emphasized = NEW_MEMBER_STATES, []
      data = data_source[data_source.DECLARANT.isin(Declarants)].query('PARTNER=="{}"'.format(Partner))
      return [
          dict(
              x = YEARS,
              y = [get_first_or_none(convert_index(data.query('DECLARANT=="{}"'.format(d))['TCI_{}'.format(year)].values)) for year in YEARS],
              text = 'Trade between {} and {}'.format(d, Partner),
              mode = 'lines',
              line = {'width': 1},
              marker = {
                  'size': 15,
                  'line': {'width': 1}
              },
              name = d
          )
          for d in Declarants]


  def update_figure(selected):
      return prepare_data(data_source, selected)


  if __name__ == '__main__':
    heatmap = {}
    slopechart = {}
    for year in YEARS:      
      x, y, z = update_figure(year)  
      heatmap[year] = dict(x=x, y=y, z=z)

    for country in PARTNERS:
      slopechart[country] = update_slopechart(country)

    json.dump(heatmap, open('output/heatmap_{}.json'.format(str_list[i]), 'w'))
    json.dump(slopechart, open('output/slopechart_{}.json'.format(str_list[i]), 'w'))
    json.dump(PARTNERS, open('output/partners_{}.json'.format(str_list[i]), 'w'))
    json.dump(NEW_MEMBER_STATES, open('output/new_member_states_{}.json'.format(str_list[i]), 'w' ))
    json.dump(YEARS, open('output/years_{}.json'.format(str_list[i]), 'w' ))
    i = i + 1
