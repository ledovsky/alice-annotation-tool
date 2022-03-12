import React from 'react';
import { DocsTitle, DocsHeader, DocsParagraph } from '../common/DocsCommon';

function DatasetsAdults (props) {
  return (
    <>
      <DocsTitle>Dataset "Adults"</DocsTitle>
      <DocsHeader>Data acquisition</DocsHeader>
      <DocsParagraph>Dataset was obtained from 21 healthy subjects. The auditory odd-ball paradigm was applied during EEG recording where the standard stimulus was short 1000Hz signal (80%), and deviant stimuli were 1020Hz (10%) and 980Hz (10%). The duration of the signal was 50 ms and the interstimulus interval was 400ms.</DocsParagraph>
      <DocsParagraph>Electroencephalography data were recorded using the NeuroTravel amplifier (EB Neuro, Italy) with sampling rate 500 Hz, and with 31-scalp electrodes arranged according to the international 10–10 system</DocsParagraph>
      <DocsParagraph>Ear lobe electrodes were used as reference, and the grounding electrode was placed centrally on the forehead.</DocsParagraph>
      <DocsHeader>Data Preprocessing</DocsHeader>
      <DocsParagraph>Obtained data were filtered (0.1 - 40 Hz) and divided into epochs (-500; 800 s) where noisy epochs were removed by threshold (350 mV). Only first 650 epochs were used for posterior ICA decomposition (FASTICA) with resampling on the level of 250 Hz. Final data consisted of 30 ICA components and uploaded into ALICE. All preprocessing steps were done using MNE Python package.</DocsParagraph>
    </>
  )
}

export default DatasetsAdults;