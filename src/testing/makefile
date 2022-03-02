DATE=$(shell date "+%a, %b %e %l:%M %p")
SRCDIR=.
OUTDIR=scratch
PROJDIR=${OUTDIR}
DEF_FONT=courier

# tools
OVERVIEW=omsview

test:
	@mkdir -p ${OUTDIR}
	@mkdir -p ${PROJDIR}
	# test manuscript WITH table of contents 
	${OVERVIEW} --manuscriptfile ${SRCDIR}/manuscript.yaml --pdffile test.courier.pdf --workdir ${PROJDIR} --matrix 5 5 --fill 200 10 10 50

	# test manuscript WITHOUT table of contents 
	${OVERVIEW} --manuscriptfile ${SRCDIR}/manuscript.yaml --pdffile test.courier.notoc.pdf --workdir ${PROJDIR}

clean:
	rm -rf ${OUTDIR}
