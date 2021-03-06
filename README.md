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


## Details on computation
- Always use one side of transaction only. Exports or imports. Create index for both.
- For comparability, aggregate up all values to 6-digit Harmonized System.
- Shares are based on value. Value of HS6 product exports between i and j in year t, divided by total value of exports between i and j.
- First baseline is EU total. Create the same shares with i = EU rather than an individual country. Drop all products that are zero in total EU trade, they will also be zero in individual countries.
- When calculating formula, treat `0 log(0) = 0` (L'Hopital's rule).

## Computation in pesudocode
```
export_ijct = zeros(N_reporter, N_partner, N_cn8, T)
export_ijpt = sum(export_ijct) by(ijt, HS6)
# include all zeros
country_share_ijpt = export_ijpt ./ sum(export_ijpt, p)
eu_share = sum(export_ijpt, i) ./ sum(export_ijpt, ip)
function KLD(x, y)
  return sum(x .* log.(x ./ y), p)
end
```

# Countries of focus
## New Member States
- Czech Republic
- Hungary
- Poland
- Slovenia
- Slovakia
- Latvia
- Lithuania
- Croatia
- Bulgaria
- Romania

## Candidate Countries
- Albania
- Bosnia
- Turkey
- Macedonia
- Montenegro
- Serbia

## Southern Neighbourhood Countries
- Algeria
- Morocco
- Tunisia

## Eastern Neighbourhood Countries
- Armenia
- Azerbaijan
- Georgia
- Moldova
- Ukraine

# Data cleaning steps
1. Data is downloaded from Eurostat Comext at [URL]
2. We only keep trade flows in normal statistical regime (excluding, for example, processing trade)
3. We aggregate all trade flows up to 6-digit Harmonized System products.
4. There are cases when product codes are masked to protect confidentiality of individual sellers, affecting about 2--3 percent of trade value. Because these product codes are available at the Chapter (2-digit) level, we redistribute the total value of confidential trade across the reported, non-confidential product codes of the same Chapter.

# State of the art

All indexes of similarity start with a vector of trade shares si and sj and compute
```
sum_p f(s_{ip}, s_{jp}),
```
for various functions $f$.

The Krugman Specialization Index (Krugman, 1991) uses $f(x, y) = |x - y|$. This index captures the absolute percentage deviation between trade shares.

An alternative measure is the Finger-Kreining index (Finger and Kreinin, 1979), with $f(x) = min(x, y)$, capturing the least amount of overlap between the two trade shares.

Fontagné et al (2018) use dissimularity measures for binary vectors, with $s_{ip}\in \{0,1\}$, such as the Levenshtein distance and the Bray-Curtis measure.

None of these indexes are based on economic theory. By contract assume that consumers have CES preferences over the individual products, with elasticity of substitution sigma. 
```
f(x, y) = x^{1/\sigma} y^{1-1/\sigma}
```
In the limite, when $\sigma\to 1$, this index converges to the Kullback-Leibler divergence.

Krugman, Paul. 1991. Geography and Trade. Cambridge: MIT Press.

Finger, J. M., and M. E. Kreinin. 1979. “A Measure of 'Export Similarity' and Its Possible Uses.” The Economic Journal 89 (356): 905–12.

Fontagné, Lionel, Angelo Secchi, and Chiara Tomasi. 2018. “Exporters’ Product Vectors across Markets.” European Economic Review 110 (November): 150–80.

