import React from 'react';
import { DocsTitle, DocsHeader, DocsParagraph } from '../common/DocsCommon';

function DatasetsMuRhythm2 (props) {
  return (
    <>
      <DocsTitle>Dataset "Mu Rhythm 2"</DocsTitle>
      <DocsHeader>Data acquisition</DocsHeader>
      <DocsParagraph>The dataset was obtained from 13 typically developing children.</DocsParagraph>
      <DocsParagraph>A 28-channel "Neurotravel" amplifier was used for EEG registration. Recording was carried out according to the international system 10-20%, reference electrodes were placed at the ear lobes (A1, A2) and their average was used as an on-line reference. Electrode impedances were kept below 15 kOm. The EEG was recorded using the Neurolab software. Recording sampling rate was 250 or 500 Hz.</DocsParagraph>
      <DocsParagraph>The experimental session included conditions with closed eyes, passive opening and closing a palm and the control condition while children were watching cartoons with no sound.</DocsParagraph>
      <DocsHeader>Data Preprocessing</DocsHeader>
      <DocsParagraph>The EEG data preprocessing was conducted in Matlab. Each EEG recording was filtered with FIR-filter in range 3-40 Hz. Artifactual 200 ms epochs were rejected with the boundary of 5 standard deviations, retaining not less than 87,4% of data. The AMICA algorithm was used for ICA decomposition with one or two models. In case of two model option, highly improbable data points were taken by the second model, thus eliminating artefacts.</DocsParagraph>
      <DocsParagraph>Final data consisted of 28 ICA components and uploaded into ALICE.</DocsParagraph>
    </>
  )
}

export default DatasetsMuRhythm2;