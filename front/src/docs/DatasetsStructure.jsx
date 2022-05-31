import React from 'react';
import { DocsTitle, DocsHeader, DocsParagraph } from '../common/DocsCommon';

function DatasetsStructure (props) {
  return (
    <>
      <DocsTitle>Download files structure</DocsTitle>
      <DocsParagraph>Each of the downloadable archives contain multiple files in csv format.</DocsParagraph>

      <DocsHeader>ics.csv</DocsHeader>
      <DocsParagraph>List of components ids with and sampling frequency rates.</DocsParagraph>
      <DocsParagraph>
        <ul className="list-disc list-inside">
          <li>ic_id - component id. For example, components with id 11 will be marked as IC000011</li>
          <li>sfreq - sampling frequency in Hz</li>
        </ul>
      </DocsParagraph>
      
      <DocsHeader>annotations_raw.csv</DocsHeader>
      <DocsParagraph>Table with unique annotations that were done by experts.</DocsParagraph>
      <DocsParagraph>
        <ul className="list-disc list-inside">
          <li>ic_id - id component id. See ics.csv</li>
          <li>user_hash - encrypted login of user</li>
          <li>flag_brain - true/false. True if IC was marked as brain activity</li>
          <li>flag_alpha - true/false. True if IC was marked as alpha activity</li>
          <li>flag_mu - true/false. True if IC was marked as mu activity</li>
          <li>flag_eyes - true/false. True if IC was marked as eyes class</li>
          <li>flag_eyes_h - true/false. True if IC was marked as horizontal eyes class</li>
          <li>flag_eyes_v - true/false. True if IC was marked as vertical eyes class</li>
          <li>flag_muscles - true/false. True if IC was marked as muscles class</li>
          <li>flag_heart - true/false. True if IC was marked as heart class</li>
          <li>flag_line_noise - true/false. True if IC was marked as line noise class</li>
          <li>flag_ch_noise - true/false. True if IC was marked as channel noise class</li>
          <li>flag_uncertain - true/false. True if IC was marked as uncertain class</li>
          <li>flag_other - true/false. True if IC was marked as other class</li>
        </ul>
      </DocsParagraph>


      <DocsHeader>[ic_id]_weights.csv</DocsHeader>
      <DocsParagraph>This file exists for each of ICs. List of channels and their weighs in component.</DocsParagraph>
      <DocsParagraph>
        <ul className="list-disc list-inside">
          <li>ch_name - EEG channel name</li>
          <li>value - weight value of  channel in component</li>
        </ul>
      </DocsParagraph>

      <DocsHeader>[ic_id]_weights.csv</DocsHeader>
      <DocsParagraph>This file exists for each of ICs. IC time series</DocsParagraph>
      <DocsParagraph>
        <ul className="list-disc list-inside">
          <li>epoch - id of epoch (if applicable)</li>
          <li>value</li>
        </ul>
      </DocsParagraph>
    </>
  )
}

export default DatasetsStructure;