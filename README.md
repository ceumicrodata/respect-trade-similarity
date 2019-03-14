# Create Dataset for Computing the Trade Similarity Index
> We will use detailed product-level trade data to construct a Trade Coherence Index for each new Member State that has acceded to the EU since 1995. This involves measuring how the external export and import structure towards third countries changed upon joining. The index will capture the relevant economic structure of the Member States (for exports) and changes in applied external tariffs (for imports). Data on the pre-EU period and post EU accession period can be used to identify the revealed comparative advantage of each country, whereas the degree of change that is observed in trade patterns can help identify the degree of incoherence. The value of the index of export-import incoherence for a newly acceded country and it main trade partners outside the EU is an indicator of the strength of the incentives for countries to use national trade and investment promotion instruments to offset at least to some extent the effects of adopting the common commercial policy of the EU. We hypothesize that the index value is a predictor for the behaviour of national trade promotion agencies and export credit agencies. This will be tested by collecting and harmonizing indicators on the mandate, size and activities of trade credit, trade promotion and investment promotion agencies. The trade coherence indicator will provide valuable information on changes in trade coherence over time and the incentives for national agencies to pursue idiosyncratic policies.

- Research data sources on country-country-product trade. EU COMEXT and UN Comtrade.
- Target sample (but download as much data as you can):
	- New EU Member States since 1995
	- Non-EU countries of special interest to RESPECT project
	- old-EU average
	- total EU average
	- at least 3 years prior to accession, up to current year
	- all products for which tariffs can be different (8-digit Combined Nomenclature classification)
- Write scripts (bash or python) to automatically download necessary data from statistical agencies. Store in meaningful folder structure, preferably as .csv file
- Create descriptive statistics of sample coverage: number of reporting countries, traded products over time.

For each country pair (say, Hungary-Russia) in each year will construct indexes of the following form:
```
TCI(i,j,t) = sum_{product p} product_share(i,j,t) * log[product_share(i,j,t) / product_share(baseline,j,t)]	
```
This is the [Kullback-Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)between the product shares (i,j) and the product shares (baseline,j). The use of KLD can (hopefully) also be motivated by economic theory. The baseline can be EU average of country-i trade shares before accession.




----------------------------------------------
Requirements:
Ubuntu:
p7zip-full
