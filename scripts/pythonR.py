#!/usr/bin/python



def DESeq_se():
   print('''#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
library("DESeq2")
library("ggplot2")
#cd1 <- read.table("samples", sep = " ", skip = 1)
cd1 <- read.table(args[1], sep = " ", skip = 1)
coldata1 <-  data.frame(row.names=cd1$V3,cd1$V4)
#dat <- read.table("test.csv",row.names=1,sep=",", TRUE)
#param <- read.table("param.input", sep = " ", fill = TRUE)
param <- read.table(args[2], sep = " ", fill = TRUE)
fl = gsub("[[:blank:]]", "", param$V2[which('COUNTFILE' == param$V1)])
dat <- read.table(fl,sep=",", TRUE)
cols = seq(8,(8+((dim(dat)[2]-7)/2))-1,1)
countdata<-dat[1:(dim(dat)[1]),cols]
lcd <- stack(log(dat[1:(dim(dat)[1]),cols]))
lcd[mapply(is.infinite, lcd)] <- NA
colnames(lcd) <- c("Count", "Conditions")
plcd=seq(1,(dim(lcd)[2] * 2),by=2)
pdf("correlation.pdf")
#p <- ggplot(lcd, aes(x = Conditions, y = Count), at=plcd) + geom_boxplot(notch=TRUE, fill='#A4A4A4', color="black")
p <- ggplot(lcd, aes(x = Conditions, y = Count, fill=Conditions), at=plcd) + geom_boxplot(notch=TRUE, color="black")
#p + geom_jitter(shape=16, position=position_jitter(0.2), col="#999999")
#p + geom_jitter(alpha=0.3, shape=16, position=position_jitter(0.2), col="#999999")
p + geom_jitter(aes(color = Conditions), alpha=0.3, shape=16, position=position_jitter(0.2))
dev.off()
pdf("correlation_violin.pdf")
p <- ggplot(lcd, aes(x = Conditions, y = Count, fill=Conditions), at=plcd) +  geom_violin(trim = FALSE)
#p + geom_jitter(color = "#999999", alpha=0.1, shape=16, position=position_jitter(0.2))
p + geom_jitter(alpha=0.1, shape=16, position=position_jitter(0.2))
dev.off()
dds=DESeqDataSetFromMatrix(countData=countdata,colData=coldata1,design=~cd1.V4)
dds2 <- DESeq(dds)
res <- results(dds2)
pdf("MA-plot.pdf")
plotMA( res, ylim = c(-1, 1) )
dev.off()

pdf("DESeq-Volcano.pdf")
par(mar=c(5,5,5,5), cex=1.0, cex.main=1.4, cex.axis=1.4, cex.lab=1.4)
topT <- as.data.frame(res)
#Adjusted P values (FDR Q values)
with(topT, plot(log2FoldChange, -log10(padj), pch=20, main="Volcano plot", cex=1.0, xlab=bquote(~Log[2]~fold~change), ylab=bquote(~-log[10]~Q~value)))
with(subset(topT, padj<0.05 & abs(log2FoldChange)>2), points(log2FoldChange, -log10(padj), pch=20, col="red", cex=0.5))
#with(subset(topT, padj<0.05 & abs(log2FoldChange)>2), text(log2FoldChange, -log10(padj), labels=subset(rownames(topT), topT$padj<0.05 & abs(topT$log2FoldChange)>2), cex=0.8, pos=3))
#Add lines for absolute FC>2 and P-value cut-off at FDR Q<0.05
abline(v=0, col="black", lty=3, lwd=1.0)
abline(v=-2, col="black", lty=4, lwd=2.0)
abline(v=2, col="black", lty=4, lwd=2.0)
abline(h=-log10(max(topT$pvalue[topT$padj<0.05], na.rm=TRUE)), col="black", lty=4, lwd=2.0)
dev.off()

pdf("pValue-histogram.pdf")
df <- data.frame(pn=factor(rep("P",each=dim(res)[1])), pvalue=res$pvalue)
#hist( res$pvalue, breaks=20, col="grey" )
ggplot(df, aes(x=pvalue)) + geom_histogram(aes(y=..density..), colour="black", fill="white") + geom_density(alpha=.2, fill="#FF6666") + ggtitle("pValue histogram") + theme(plot.title = element_text(size = rel(1.5), hjust = 0.5),axis.title = element_text(size = rel(1.25)))
dev.off()
rld <- rlogTransformation(dds, blind=TRUE)
data <- plotPCA(rld, intgroup=c("cd1.V4"),returnData=TRUE)
percentVar <- round(100 * attr(data,"percentVar"))
pdf("pca.pdf")
#ggplot(data, aes(x=PC1, y=PC2, color=group)) + geom_point(shape=23, fill="blue", color="darkred", size=3)
ggplot(data, aes(x=PC1, y=PC2, color=group)) + geom_point(shape=19, size=3) + ggtitle("PCA plot") + theme(plot.title = element_text(size = rel(1.5), hjust = 0.5),axis.title = element_text(size = rel(1.25)))
dev.off()''')


DESeq_se()
