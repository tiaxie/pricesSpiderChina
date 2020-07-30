# pricesSpiderChina
A spider that scrapes price information of major Chinese eCommerce sites(tmall, jingdong, suning, dangdang)

#Your input for the product you want to scrape data of
To run the spider, first go to tmallspider/tmallspider/spiders/spiders.py
For line 25, you will see the variable s_input. Modify this variable to whatever product you want to scrape. 

#To run the spider
1. run spiders.py
2. run dataProcess.py
Then the price information of the product (as well as any promotion activities) will be generated in a excel file called "output.xlsx" under your current directory

#Potential improvements
For now, the spider can only scrape the information of one product at a time. You need to modify "s_input" for a new product that you want the information of
