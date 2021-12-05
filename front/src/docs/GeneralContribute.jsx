import React from 'react';
import { DocsTitle, DocsParagraph } from '../common/DocsCommon';
import ExternalLink from '../common/ExternalLink';

function GeneralContribute (props) {
  return (
    <>
      <DocsTitle>How to contribute</DocsTitle>
      <DocsParagraph>There are mainly two ways how you can contribute to the project</DocsParagraph>
      <DocsParagraph>Become the ALICE expert and make annotations for ICA data</DocsParagraph>
      <DocsParagraph>Share your dataset so our models could be trained on new types of ICA components.</DocsParagraph>
      <DocsParagraph>Contact us via an email <ExternalLink href="mailto:alexander.ledovsky@gmail.com">alexander.ledovsky@gmail.com</ExternalLink> and <ExternalLink href="mailto:gsogoyan98@gmail.com">gsogoyan98@gmail.com</ExternalLink> to know more about our policy and become part of the ALICE project!</DocsParagraph>
    </>
  )
}

export default GeneralContribute;