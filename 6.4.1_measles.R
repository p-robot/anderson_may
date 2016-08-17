tmp <- ts(log(df$cases), start = c(1948,1), end = c(1966,11), 
deltat = 1/52)

#plot(tmp)

spectrum(tmp, detrend = TRUE, demean = TRUE, 
    spans = c(3, 7, 9))

