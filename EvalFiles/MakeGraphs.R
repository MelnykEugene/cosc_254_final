Mushroom <- read.csv("Mushroom-Mushroom.csv")
T10 <- read.csv("T10-T10.csv")

Mushroom <- Mushroom %>%
  mutate(Algorithm = Algo) %>%
  select(FreqThresh, Algorithm, Average, Memory)
T10 <- T10 %>%
  mutate(Algorithm = Algo) %>%
  select(FreqThresh, Algorithm, Average, Memory)

ggplot(data=Mushroom, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for Mushroom.dat") + ylab("Log Average Runtime (s)") + xlab("Minimum Frequency Threshold") + scale_y_continuous(trans="log10")
ggsave("LogMushRun.png")

ggplot(data=Mushroom, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for Mushroom.dat") + ylab("Average Runtime (s)") + xlab("Minimum Frequency Threshold")
ggsave("FullMushRun.png")

MushroomZoomed <- Mushroom %>%
  filter(FreqThresh > .4)

ggplot(data=MushroomZoomed, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for Mushroom.dat") + ylab("Average Runtime (s)") + xlab("Minimum Frequency Threshold")
ggsave("Zoom2MushRun.png")

MushroomZoomed <- Mushroom %>%
  filter(FreqThresh < .4)

ggplot(data=MushroomZoomed, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for Mushroom.dat") + ylab("Average Runtime (s)") + xlab("Minimum Frequency Threshold")
ggsave("Zoom1MushRun.png")

Mush_Memory <- ggplot(data=Mushroom, aes(x=FreqThresh, y = Memory, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Memory Usage for Mushroom.dat") + ylab("Memory Used (MB)") + xlab("Minimum Frequency Threshold")
ggsave("MushMemory.png")



T10Zoomed <- T10 %>%
  filter(FreqThresh < .15)

ggplot(data=T10Zoomed, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for T10I4D100K.dat") + ylab("Log Average Runtime (s)") + xlab("Minimum Frequency Threshold")+ scale_y_continuous(trans="log10")
ggsave("LogZoomT10Run.png")

T10Zoomed2 <- T10Zoomed %>%
  filter(Algorithm != "Apriori")

ggplot(data=T10Zoomed2, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for T10I4D100K.dat") + ylab("Average Runtime (s)") + xlab("Minimum Frequency Threshold")
ggsave("ZoomNoAprioriT10Run.png")

ggplot(data=T10, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for T10I4D100K.dat") + ylab("Average Runtime (s)") + xlab("Minimum Frequency Threshold")
ggsave("FullT10Run.png")

ggplot(data=T10, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for T10I4D100K.dat") + ylab("Log Average Runtime (s)") + xlab("Minimum Frequency Threshold")+ scale_y_continuous(trans="log10")
ggsave("LogT10Run.png")

ggplot(data=T10Zoomed, aes(x=FreqThresh, y = Memory, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Memory Usage for T10I4D100K.dat") + ylab("Memory Used (MB)") + xlab("Minimum Frequency Threshold")
ggsave("T10Memory.png")

T10Zoomed <- T10 %>%
  filter(FreqThresh > .15)
ggplot(data=T10Zoomed, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for T10I4D100K.dat") + ylab("Log Average Runtime (s)") + xlab("Minimum Frequency Threshold")+ scale_y_continuous(trans="log10")
ggsave("LogZoom2T10Run.png")

ggplot(data=T10Zoomed, aes(x=FreqThresh, y = Average, color = Algorithm))+ geom_point() + geom_line() + ggtitle("Runtimes for T10I4D100K.dat") + ylab("Average Runtime (s)") + xlab("Minimum Frequency Threshold")
ggsave("FullZoomT10Run.png")