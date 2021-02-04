#!/usr/bin/env nextflow
/*
========================================================================================
                        Metagenomic_analysis
========================================================================================
*/

def helpMessage() {
    log.info nfcoreHeader()
    log.info"""
    Usage:

    The typical command for running the pipeline is as follows:
      nextflow run src/metaG_analysis.nf -c src/metaG_analysis.config --fromSRA ["A","B","C"] --fromPATH ["A","B","C"] -profile singularity


    Required arguments:
      --inputFromSRA                Specify SRA IDs fastq files data (required if --fromPATH not specified)
      --inputFromPATH               Directory pattern for fastq files: (required if --fromSRA not specified)
                                    Please use following syntax for paired end data : data/filePE_R{1,2}*.fastq
    Reference DB
      --fasta                       Full path to directory containing genome fasta file


    QC Option:
      --skipFastqc                  Skip reads quality control step (default: activated).
      --skipMultiqc                 Skip merging tools reports suitable with multiqc (default: activated)

    Trimming option:
      --trimming                    Activated trimming step (default: desactivated)
      --adapter_removal             Activated adapter removal step (default: desactivated)

    Nextflow config:
      -c                            Path to config file: src/chip_analysis.config
      -profile                      Profil used by nextflow to run the pipeline (you have choice between singularity, docker, psmn or ccin2p3)
                                    For local utilisation use singularity or docker
    Save option:
      --outdir                      Specify where to save the output from the nextflow run (default: "./results/")

    help message:
      --help                        Print help message
    """
      .stripIndent()
  }


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
/* --                                                                     -- */
/* --                SETUP CONFIGURATION VARIABLES                       -- */
/* --                                                                     -- */
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////




////////////////////////////////////////////////////
/* --         DEFAULT PARAMETER VALUES         -- */
////////////////////////////////////////////////////
params.help = false
params.trimming = false
params.adapter_removal = false
params.skipFastqc = false
params.skipMultiqc = false
params.inputFromPATH = false
params.inputFromSRA = false
params.outdir = 'results'


/*
 * SETUP CONFIGURATION VARIABLES
 */

// Show help message
if (params.help) {
    helpMessage()
    exit 0
}

////////////////////////////////////////////////////
/* --          VALIDATE INPUTS                 -- */
////////////////////////////////////////////////////

if (!params.inputFromSRA && !params.inputFromPATH){  exit 1, "Input params not specified!\nUse --help" }

//if (params.fasta) {
//        Channel
//            .fromPath( params.fasta )
//            .ifEmpty { error "Cannot find any fasta files matching: ${params.fasta}" }
//            .set { fasta_file }
//}
//else { exit 1,
/*
  log.warn "=================================================================\n" +
           "  WARNING! No genome fasta file precised.\n" +
           "  Use '--fasta' \n" +
           "  Or '--help' for more informations"
           "======================================================================="
}
*/

if (params.inputFromSRA){
        Channel
            .fromSRA(params.inputFromSRA, apiKey:'6e15df3377f722be16ef0e546d8a40982808')
            .ifEmpty { error "Cannot find any SRA IDs matching: ${params.inputFromSRA}" }
            .set{ fastq_fromSRA }
}
else{
        Channel
            .empty()
            .set { fastq_fromSRA }

}

if (params.inputFromPATH){
        Channel
            .fromFilePairs(params.inputFromPATH, size:-1)
            .ifEmpty { error "Cannot find any file matching: ${params.inputFromPATH}" }
            .set{ fastq_fromPATH }
}
else{
        Channel
            .empty()
            .set { fastq_fromPATH }
}


/*
* CONCAT fromPath and fromSRA channels into a single input channel
*/
fastq_fromPATH
              .concat(fastq_fromSRA)
              .into{ fastq_raw_2QC ; fastq_raw_2trim  }



  ///////////////////////////////////////////////////////////////////////////////
  ///////////////////////////////////////////////////////////////////////////////
  /* --                                                                     -- */
  /* --                       HEADER LOG INFO                               -- */
  /* --                                                                     -- */
  ///////////////////////////////////////////////////////////////////////////////
  ///////////////////////////////////////////////////////////////////////////////

  // Header log info
  log.info nfcoreHeader()
  def summary = [:]
  summary['From SRA']               = params.inputFromSRA ? params.inputFromSRA : 'Not supplied'
  summary['From PATH']              = params.inputFromPATH ? params.inputFromPATH : 'Not supplied'
  summary['Remove Adapter']         = params.adapter_removal ? 'Yes' : 'Skipped'
  summary['Trimming']               = params.trimming ? 'Yes': 'Skipped'
  summary['Reads QC']               = params.skipFastqc ? 'Skipped' : 'Yes'
  summary['Merging Reports']        = params.skipMultiqc ? 'Skipped' : 'Yes'
  summary['Config Profile']         = workflow.profile
  summary['Output']                 = params.outdir
  log.info summary.collect { k,v -> "${k.padRight(20)}: $v" }.join("\n")
  log.info "-\033[2m--------------------------------------------------\033[0m-"



  ///////////////////////////////////////////////////////////////////////////////
  ///////////////////////////////////////////////////////////////////////////////
  /* --                                                                     -- */
  /* --                         TRIMMING READS                              -- */
  /* --                                                                     -- */
  ///////////////////////////////////////////////////////////////////////////////
  ///////////////////////////////////////////////////////////////////////////////

  if (!params.trimming) {
       fastq_raw_2trim.set{fastq_trim_2cutAdapt }
       Channel
              .empty()
              .set { fastq_trim_2QC }

       Channel
              .empty()
              .set { trimming_report }
    }
  else {
      process Trimming {
        label "cutadapt"
        tag "$file_id"
        publishDir "${params.outdir}/fastq/trim/", mode: 'copy'

        input:
        set file_id, file(reads) from fastq_raw_2trim

        output:
        set file_id, "${file_id}*_trim.fastq.gz" into fastq_trim_2QC, fastq_trim_2cutAdapt
        set file_id, "${file_id}*_report.txt" into trimming_report

        script:
        def single = reads instanceof Path

        if (single){
        """
          cutadapt -q 20,20 \
          -o ${file_id}_trim.fastq.gz \
          ${reads} > ${file_id}_report.txt
        """
        }
        else{
        """
        cutadapt -q 20,20 \
        -o ${file_id}_R1_trim.fastq.gz -p ${file_id}_R2_trim.fastq.gz \
        !{reads[0]} ${reads[1]} > ${file_id}_report.txt
        """
        }
      }
  }

 ///////////////////////////////////////////////////////////////////////////////
 ///////////////////////////////////////////////////////////////////////////////
 /* --                                                                     -- */
 /* --                         REMOVE ADAPTERS                             -- */
 /* --                                                                     -- */
 ///////////////////////////////////////////////////////////////////////////////
 ///////////////////////////////////////////////////////////////////////////////

 if (!params.adapter_removal) {
       fastq_trim_2cutAdapt.set{ fastq_2assembly}
       Channel
              .empty()
              .set { fastq_cutAdapt_2QC }
       Channel
             .empty()
             .set { adapter_removal_report }
   }
 else {
     process Adapter_removal {
       label "cutadapt"
       tag "$file_id"
       publishDir "${params.outdir}/fastq/cut/", mode: 'copy'

       input:
       set file_id, file(reads) from fastq_trim_2cutAdapt

       output:
       set file_id, "${file_id}*_cut.fastq.gz" into fastq_2assembly, fastq_cutAdapt_2QC
       set file_id, "${file_id}_report.txt" into adapter_removal_report

       script:
       def single = reads instanceof Path

       if (single){
       """
       cutadapt -a AGATCGGAAGAG -g CTCTTCCGATCT\
       -o ${file_id}_cut.fastq.gz \
       ${reads} > ${file_id}_report.txt
       """
       }
       else{
       """
       cutadapt -a AGATCGGAAGAG -g CTCTTCCGATCT -A AGATCGGAAGAG -G CTCTTCCGATCT \
       -o ${file_id}_R1_cut.fastq.gz -p ${file_id}_R2_cut.fastq.gz \
       ${reads[0]} ${reads[1]} > ${file_id}_report.txt
       """
       }
 }
 }

 ///////////////////////////////////////////////////////////////////////////////
 ///////////////////////////////////////////////////////////////////////////////
 /* --                                                                     -- */
 /* --                       READS QUALITY CONTROLE                        -- */
 /* --                                                                     -- */
 ///////////////////////////////////////////////////////////////////////////////
 ///////////////////////////////////////////////////////////////////////////////


 /*
  * CONCAT RAW, TRIM, CUTADAPT FASTQ INTO SINGLE Channel
  */
 fastq_raw_2QC
             .concat(fastq_trim_2QC)
             .concat(fastq_cutAdapt_2QC)
             .set{fastq_2QC}


 if (params.skipFastqc) {
         Channel
               .empty()
               .set { fastqc_report }
 }
 else{
     process Fastqc {
          label "fastqc"
          tag "$file_id"
          publishDir "${params.outdir}/${file_id}/QC/", mode: 'copy'

          input:
          set file_id, file(reads) from fastq_2QC

          output:
          file "*.{zip,html}" into fastqc_report

          script:
          def single = reads instanceof Path

          if (single){
             """
             fastqc --quiet --threads ${task.cpus} --format fastq --outdir ./ \
             ${reads}
             """
           }
         else{
             """
             fastqc --quiet --threads ${task.cpus} --format fastq --outdir ./ \
             ${reads[0]} ${reads[1]}
             """
           }
    }
 }



// A priori, spade a besoin de virer les reads non pairé
// vérifier l'effet
//car sans le faire ça marche !
/*

 process Keep_reads_paired {
      label "fastq_pair"
      tag "$file_id"
      publishDir "${params.outdir}/${file_id}/read_paired/", mode: 'copy'

      input:
      set file_id, file(reads) from fastq_2assembly

      output:
      set file_id, "*.paired.fq" into fastq_ready2assembly

      script:
      def single = reads instanceof Path

      if (single){
        log.warn "=================================================================\n" +
                 "  WARNING! ${file_id} seems to be a Single-End library\n" +
                 "  Only one file links to {file_id}: ${reads}\n" +
                 "  MetaSpades need Paired-End data"
                 "======================================================================="
       }
     else{
         """
         zcat ${reads[0]} > ${reads[0].simpleName}
         zcat ${reads[1]} > ${reads[1].simpleName}
         fastq_pair ${reads[0].simpleName} ${reads[1].simpleName}
         """
       }
 }
 */



 process Assembly {
      label "spades"
      tag "$file_id"
      publishDir "${params.outdir}/${file_id}/assembly", mode: 'copy'

      input:
      set file_id, file(reads) from fastq_2assembly

      output:
      file "*" into spades_files
      set file_id, "scaffolds.fasta" into scaffolds

      script:
      def single = reads instanceof Path

      if (single){
        log.warn "=================================================================\n" +
                 "  WARNING! ${file_id} seems to be a Single-End library\n" +
                 "  Only one file links to {file_id}: ${reads}\n" +
                 "  MetaSpades need Paired-End data"
                 "======================================================================="
       }
     else{
         """
         spades.py -t ${task.cpus} -m 100 \
         --pe1-1 ${reads[0]} \
         --pe1-2 ${reads[1]} \
         -o ./
         """
       }
}

process Quast {
     label "quast"
     tag "$file_id"
     publishDir "${params.outdir}/${file_id}/assembly/quast", mode: 'copy'

     input:
     set file_id, file(scaff) from scaffolds

     output:
     file "*" into quast_report

     script:
        """
        quast.py -t ${task.cpus} -o ./ \
        ${scaff}
        """
}
 ///////////////////////////////////////////////////////////////////////////////
 ///////////////////////////////////////////////////////////////////////////////
 /* --                                                                     -- */
 /* --                       NF-CORE HEADER                                -- */
 /* --                                                                     -- */
 ///////////////////////////////////////////////////////////////////////////////
 ///////////////////////////////////////////////////////////////////////////////

 def nfcoreHeader() {
     // Log colors ANSI codes
     c_reset =  "\033[0m";
     c_dim = "\033[2m";
     c_black = "\033[0;30m";
     c_green = "\033[0;32m";
     c_yellow = "\033[0;33m";
     c_blue = "\033[0;34m";
     c_purple = "\033[0;35m";
     c_cyan = "\033[0;36m";
     c_white ="\033[0;37m";

     return """    -${c_dim}--------------------------------------------------${c_reset}-
                                             ${c_green},--.${c_black}/${c_green},-.${c_reset}
     ${c_blue}        ___     __   __   __   ___     ${c_green}/,-._.--~\'${c_reset}
     ${c_blue}  |\\ | |__  __ /  ` /  \\ |__) |__         ${c_yellow}}  {${c_reset}
     ${c_blue}  | \\| |       \\__, \\__/ |  \\ |___     ${c_green}\\`-._,-`-,${c_reset}
                                             ${c_green}`._,._,\'${c_reset}
     ${c_purple}  METAG Pipeline          ${c_reset}
     -${c_dim}--------------------------------------------------${c_reset}-
     """.stripIndent()
 }
