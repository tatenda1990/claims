# Claims MicroProject
### Working with JSON files

There was need to cross reference location claims that were made to weather the people submitting said claims had acually visited said places. Numerous approaches were discussed until the best available solution was determined to be one in which location data could be checked against the dates in which claims of presence were made. As such Google Maps data was downloaded for affected persons over the time region (May 2022 to August 2022). 

### Data Aquisition

Google Maps Data, ordinarily available through the timeline feature in maps, was downloaded. For this https://takeout.google.com/ was used by affected individuals to download their location data. JSON files for the required month were then obtained and the scipt caters for processing these data into a dataframe. The claimed dates on the location were collated into an csv file

### Processing

A script was then written in which the data from claims.csv was compared against mined location data from downloaded Maps json files.  
