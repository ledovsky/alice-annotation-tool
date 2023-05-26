import React from 'react';
import { DocsTitle, DocsHeader, DocsParagraph } from '../common/DocsCommon';
import Link from '../common/Link';

function GeneralAbout (props) {
  return (
    <>
      <DocsTitle>About the ALICE Project</DocsTitle>
      <DocsParagraph>The ALICE project aims to develop a sustainable algorithm for EEG artifact removal and bias-free detection of oscillatory brain activity.</DocsParagraph>
      <DocsHeader>Overview</DocsHeader>
      <DocsParagraph>Independent Component Analysis (ICA) is a conventional approach to exclude non-brain signals such as eye-movements and muscle artifacts from electroencephalography (EEG). Due to other possible EEG contaminations, a rejection of independent components (ICs) is usually performed in the semiautomatic mode under researchers' visual inspection. The other important ICA application is the detection of alpha and/or mu-rhythm components in the resting-state/motor imaginary conditions. This detection is also highly dependent on the subjective expert opinion, which influences EEG data reproducibility.</DocsParagraph>
      <DocsParagraph>The ALICE toolbox aims to use 1) ICA decomposition, 2) crowdsourced expert opinions on independent components (ICs) labeling; 3) which serve for supervised machine learning models; to build sustainable automatic algorithms for: the removing artifacts from EEG visual detection of rhythmic brain activity such as the alpha and mu rhythms. </DocsParagraph>
      <DocsParagraph>The ALICE toolbox allows different researchers to compare their algorithms of IC labeling. The labeling choice is based on the estimation of IC time-series, IC amplitude topography, and spectral power distribution. Additionally, the ALICE project provides an online platform for <Link href="/docs/sharing-policy">sharing</Link> ICs and cross-reviewing of the different ICs from EEG datasets.</DocsParagraph>
      <DocsParagraph>Notably, the ALICE project focuses not only on EEG data obtained in healthy adult volunteers but also on different age groups and EEG in different neural pathology. The IC labeling in children and patient groups is challenging the IC labeling accuracy due to more prominent movement artifacts. That is why the ALICE project pays special attention to nonstandard datasets to develop more sophisticated machine learning algorithms of IC labeling.</DocsParagraph>
    </>
  )
}

export default GeneralAbout;