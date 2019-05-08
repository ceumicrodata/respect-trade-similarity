preserve 

* calculate aggregate trade share of products for each partner country
collapse (sum) value_in_euros , by(partner_iso product_nc )
egen country_total = sum(value_in_euros ), by(partner_iso )
gen eu_share = value_in_euros / country_total 

keep partner_iso product_nc eu_share 
tempfile eu_share
save `eu_share', replace

restore

egen country_total = sum(value_in_euros ), by(declarant_iso partner_iso )
gen share = value_in_euros / country_total 

merge m:1 partner_iso product_nc using `eu_share', nogen keep(match master)

* if EU share is zero, that product does not enter KLD calculation
drop if eu_share == 0
assert eu_share > 0 & !missing(eu_share)

gen KLD = share * log(share / eu_share)
* 0 log(0) = 0
replace KLD = 0 if share == 0

collapse (sum) KLD, by(declarant_iso partner_iso)

