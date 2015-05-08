library(lubridate)
library(dplyr)
library(tidyr)
times <- read.csv("./data/times.csv")

colnames(times) <- c("Fecha","Hora")
times <- data.frame(do.call(rbind, strsplit(as.vector(times$Hora), split = "_")))
times$FechaHora <- paste(times$X1, times$X2, sep=" ")

Fechas <- subset(times, select = FechaHora)

Fechas$FechaHora <- strptime(as.character(Fechas$FechaHora), format = "%Y.%m.%d %H:%M:%S")
time_series = vector(mode="integer", length=207)

for (i in 1:207 ) {
  time_series[i] <- difftime(Fechas$FechaHora[i], Fechas$FechaHora[1], units = "mins") 
}

write.table(time_series, file = "time_series.csv", row.names = FALSE, col.names = FALSE)

