import React from 'react';
import { DocsTitle, DocsParagraph } from '../common/DocsCommon';
import Link from '../common/Link';

function GeneralSharing (props) {
  return (
    <>
      <DocsTitle>Kids Dataset</DocsTitle>
      <DocsParagraph>The ALICE project allows sharing ICs and provides a cross-review platform for IC labeling. Researchers from different projects will perform IC labeling for your datasets depending on your impact on the IC labeling of the previously uploaded datasets.</DocsParagraph>
      <DocsParagraph><Link href="/docs/contribute">How to share your IC datasets</Link></DocsParagraph>
    </>
  )
}

export default GeneralSharing;