Goals: - extract an abstract of a journal article available in AEA website

Text mining with `rvest`
========================

Unfortunately, to access a journal article with URL, you need DOI and AER identifier. For instance, the URL for one of my favourite articles (Partner Choice, Investment in Children, and the Marital College Premium) by Chiappori et al. (2017) is `https://www.aeaweb.org/articles?id=10.1257/aer.20150154` where `10.1257` is DOI and `20150154` is AER identifier.

One good news is that AEA website has a user friendly URL protocol for each *issue* that was published after the winter of 2002 -- it is not difficult to see that each issue is saved as `https://www.aeaweb.org/issues/ISSUE.NUMBER` where `ISSUE.NUMBER` increases by one whenever there is a next issue for one of AER/AERInsights/AEJApplied/AEJPolicy/AEJMacro/AEJMicro/JEL/JEP. Note that the journal issue corresponding to `ISSUE.NUMBER = 1` is JEP Vol. 16 No. 1 published in Winter 2002. For expository purpose, let's focus on the journal issue with `ISSUE.NUMBER = 475` (AER Vol.107 No.8) for now. You can iterate over all issues or limit the journals of interest to one particular journal if you want.

Extracting article names and URLs from a single issue
-----------------------------------------------------

The following script extracts the HTML of the journal issue with `ISSUE.NUMBER = 475`:

``` r
# install.packages("rvest") # uncomment and run this line if rvest is not installed
# install.packages("stringi") # uncomment and run this line if stringi is not installed
library(rvest)
```

    ## Warning: package 'rvest' was built under R version 3.5.1

    ## Loading required package: xml2

    ## Warning: package 'xml2' was built under R version 3.5.1

``` r
library(stringi)

ISSUE.NUMBER <- 475
issue.html <- read_html(paste0("https://www.aeaweb.org/issues/", ISSUE.NUMBER))
```

It's time to use SelectorGadget (<https://selectorgadget.com/>) to figure out how each webpage was constructed. It is not difficult to see that - node with `section h1` contains the title of the journal (`American Economic Review`) - node with `section h2` contains the volume number and date of publication (`Vol. 107 No. 8 August 2017`) - nodes with `h3 a` contains the titles of all articles appeared in the issue (`Front Matter`, `Partner Choice, Investment in Children, and the Marital College Premium`, ...)

### Journal name

To extract the journal name,

``` r
journal.name <- issue.html %>% 
  html_nodes("section h1") %>% # access the html node with `section h1`
  html_text() # filter the html data so that we have only string data

print(journal.name)
```

    ## [1] "American Economic Review"

### Year of publication

Similarly, we can extract the year of publication.

``` r
year.of.pub <- issue.html %>% 
  html_nodes("section h2") %>% # access the html node with `section h2`
  html_text() # filter the html data so that we have only string data

print(year.of.pub) # this line contains volume #/month/year. Extract the very last word for year!
```

    ## [1] "\n            Vol. 107            No. 8             August 2017        "

Note that the text we extracted contains volume number AND month of publication AND year of publication. We can use `stringr` to extract the very last word, which is the year of publication.

``` r
year.of.pub <- stri_extract_last_words(year.of.pub) # extract the last word
print(year.of.pub)
```

    ## [1] "2017"

### Article titles

Similarly, for article titles:

``` r
article.titles <- issue.html %>% 
  html_nodes("h3 a") %>% # access the html node with `h3 a`
  html_text() # filter the html data so that we have only string data

print(article.titles)
```

    ##  [1] "Front Matter"                                                                                                 
    ##  [2] "Partner Choice, Investment in Children, and the Marital College Premium"                                      
    ##  [3] "Team Incentives and Performance: Evidence from a Retail Chain"                                                
    ##  [4] "Gender Quotas and the Crisis of the Mediocre Man: Theory and Evidence from Sweden"                            
    ##  [5] "Full Implementation and Belief Restrictions"                                                                  
    ##  [6] "Identifying and Spurring High-Growth Entrepreneurship: Experimental Evidence from a Business Plan Competition"
    ##  [7] "Multi-category Competition and Market Power: A Model of Supermarket Pricing"                                  
    ##  [8] "Stock Price Booms and Expected Capital Gains"                                                                 
    ##  [9] "Clearing Up the Fiscal Multiplier Morass"                                                                     
    ## [10] "Hayek, Local Information, and Commanding Heights: Decentralizing State-Owned Enterprises in China"

### Article URLs

Now it's time to grab article URLs from each issue! To do so, simply change `html_text()` in piping to `html_attr("href")` since we are looking for the URL that each journal article links to.

``` r
article.urls <- issue.html %>% 
  html_nodes("h3 a") %>% # access the html node with `h3 a`
  html_attr("href") # filter the html data so that we have only URL string

print(article.urls)
```

    ##  [1] "/articles?id=10.1257/aer.107.8.i" 
    ##  [2] "/articles?id=10.1257/aer.20150154"
    ##  [3] "/articles?id=10.1257/aer.20160788"
    ##  [4] "/articles?id=10.1257/aer.20160080"
    ##  [5] "/articles?id=10.1257/aer.20151462"
    ##  [6] "/articles?id=10.1257/aer.20151404"
    ##  [7] "/articles?id=10.1257/aer.20160055"
    ##  [8] "/articles?id=10.1257/aer.20140205"
    ##  [9] "/articles?id=10.1257/aer.20111196"
    ## [10] "/articles?id=10.1257/aer.20150592"

Note that the URLs we get are not the full URLs (which we need to get access to the HTML data), rather the URLs relative to the home website (`https://www.aeaweb.org/`). Hence, to get the complete URLs, we have to put `https://www.aeaweb.org` in front. To do so, use `paste0` in R. Note that `paste0` can be applied to vector too.

``` r
article.urls <- paste0("https://www.aeaweb.org", article.urls)
article.urls
```

    ##  [1] "https://www.aeaweb.org/articles?id=10.1257/aer.107.8.i" 
    ##  [2] "https://www.aeaweb.org/articles?id=10.1257/aer.20150154"
    ##  [3] "https://www.aeaweb.org/articles?id=10.1257/aer.20160788"
    ##  [4] "https://www.aeaweb.org/articles?id=10.1257/aer.20160080"
    ##  [5] "https://www.aeaweb.org/articles?id=10.1257/aer.20151462"
    ##  [6] "https://www.aeaweb.org/articles?id=10.1257/aer.20151404"
    ##  [7] "https://www.aeaweb.org/articles?id=10.1257/aer.20160055"
    ##  [8] "https://www.aeaweb.org/articles?id=10.1257/aer.20140205"
    ##  [9] "https://www.aeaweb.org/articles?id=10.1257/aer.20111196"
    ## [10] "https://www.aeaweb.org/articles?id=10.1257/aer.20150592"

### Extracting abstract

Let's read the abstract:

``` r
(read_html(article.urls[2]) %>%
  html_nodes("section section") %>%
  html_text())[3]
```

    ## [1] "Abstract\n\t\t\t\t\tWe construct a model of household decision-making in which agents consume a private and a public good, interpreted as children's welfare. Children's utility depends on their human capital, which depends on the time their parents spend with them and on the parents' human capital. We first show that as returns to human capital increase, couples at the top of the income distribution should spend more time with their children. This in turn should reinforce assortative matching, in a sense that we precisely define. We then embed the model into a transferable utility matching framework with random preferences, a la Choo and Siow (2006), which we estimate using US marriage data for individuals born between 1943 and 1972. We find that the preference for partners of the same education has significantly increased for white individuals, particularly for the highly educated. We find no evidence of such an increase for black individuals. Moreover, in line with theoretical predictions, we find that the \"marital college-plus premium\" has increased for women but not for men.\t\t\t\t"
