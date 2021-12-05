/*
Here we implement the methodology specified in the documentation
*/

import { React } from 'react';
import { useState } from 'react';

import Button from '../common/Button';
import CheckboxField from '../common/CheckboxField';


const tooltips = {
  flag_brain: "Brain activity",
  flag_alpha: "Alpha brain EEG rhythm",
  flag_mu: "Mu brain EEG rhythm",
  flag_eyes: "Eyes artefacts",
  flag_eyes_blinks: "Components that represent eye blink artefacts",
  flag_eyes_h: "Components that represent activity during eye movements in horizontal directions",
  flag_eyes_v: "Components that represent activity during eye movements in vertical directions",
  flag_noise: "Noise artefacts",
  flag_line_noise: "Line current noise that is evoked by surrounding electrical devices. Its dramatically high amplitudes well recognise it in 50 or 60 Hz",
  flag_ch_noise: "The noise associated with channels that can be marked as bad ones",
  flag_ch_noise: "The noise associated with channels that can be marked as bad ones",
  flag_muscles_and_movement: "Muscle and movements artefacts",
  flag_muscles: "Artefacts come from a recording of muscle activity on the head surface",
  flag_movement: "Artefacts that are produced by participant movements during recording",
  flag_heart: "Artefacts that represent electrocardiographic activity",
  flag_other: "Can be used to mark components as finished in case of partial annotation (e.g. eyes-only)",
  flag_uncertain: "Use in case of severly mixed components and low confidence in labels",

}


function AnnotationFormV2( props ) {

  function isValid() {
    return true;
  }

  async function onChange (e) {
    const {name, checked} = e.target;
    let upd = {};
    upd[name] = checked;
    if (name === "flag_brain" & !checked) {
      upd = {...upd, "flag_mu": false, "flag_alpha": false};
    }
    if (name === "flag_eyes" & !checked) {
      upd = {...upd, "flag_eyes_blinks": false, "flag_eyes_h": false, "flag_eyes_v": false};
    }
    if (name === "flag_muscles_and_movement" & !checked) {
      upd = {...upd, "flag_muscles": false, "flag_movement": false};
    }
    if (name === "flag_noise" & !checked) {
      upd = {...upd, "flag_line_noise": false, "flag_ch_noise": false};
    }
    props.handleCheck(upd);
  }

  return (
    <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" >
      <div className="flex">
        <p className="font-bold">Select IC classes</p>
      </div>

      {/* Brain block */}
      <CheckboxField name="flag_brain" onChange={onChange} checked={props.annotation.flag_brain} disabled={!props.loggedIn} tooltip={tooltips.flag_brain}>Brain</CheckboxField>
      { props.annotation.flag_brain ?
      <div className="ml-10">
        <CheckboxField name="flag_mu" onChange={onChange} checked={props.annotation.flag_mu} disabled={!props.loggedIn} tooltip={tooltips.flag_alpha}>Mu rhythm</CheckboxField>
        <CheckboxField name="flag_alpha" onChange={onChange} checked={props.annotation.flag_alpha} disabled={!props.loggedIn} tooltip={tooltips.flag_mu}>Alpha rhythm</CheckboxField>
      </div>
      : null
      }

      {/* Eyes block */}
      <CheckboxField name="flag_eyes" onChange={onChange} checked={props.annotation.flag_eyes} disabled={!props.loggedIn} tooltip={tooltips.flag_eyes}>Eyes</CheckboxField>
      { props.annotation.flag_eyes ?
      <div className="ml-10">
      <CheckboxField name="flag_eyes_blinks" onChange={onChange} checked={props.annotation.flag_eyes_blinks} disabled={!props.loggedIn} tooltip={tooltips.flag_eyes_blinks}>Eye Blinks</CheckboxField>
      <CheckboxField name="flag_eyes_h" onChange={onChange} checked={props.annotation.flag_eyes_h} disabled={!props.loggedIn} tooltip={tooltips.flag_eyes_h}>Eyes Horizontal</CheckboxField>
      <CheckboxField name="flag_eyes_v" onChange={onChange} checked={props.annotation.flag_eyes_v} disabled={!props.loggedIn} tooltip={tooltips.flag_eyes_v}>Eyes Vertical</CheckboxField>
      </div>
      : null
      }

      {/* Muscle and Movement block */}
      <CheckboxField name="flag_muscles_and_movement" onChange={onChange} checked={props.annotation.flag_muscles_and_movement} disabled={!props.loggedIn} tooltip={tooltips.flag_muscles_and_movement}>Muscles and Movement</CheckboxField>
      { props.annotation.flag_muscles_and_movement ?
      <div className="ml-10">
      <CheckboxField name="flag_muscles" onChange={onChange} checked={props.annotation.flag_muscles} disabled={!props.loggedIn} tooltip={tooltips.flag_muscles}>Muscles</CheckboxField>
      <CheckboxField name="flag_movement" onChange={onChange} checked={props.annotation.flag_movement} disabled={!props.loggedIn} tooltip={tooltips.flag_movement}>Movement</CheckboxField>
      </div>
      : null
      }

      <CheckboxField name="flag_heart" onChange={onChange} checked={props.annotation.flag_heart} disabled={!props.loggedIn} tooltip={tooltips.flag_heart}>Heart</CheckboxField>

      {/* Noise block */}
      <CheckboxField name="flag_noise" onChange={onChange} checked={props.annotation.flag_noise} disabled={!props.loggedIn} tooltip={tooltips.flag_noise}>Noise</CheckboxField>
      { props.annotation.flag_noise ?
      <div className="ml-10">
      <CheckboxField name="flag_ch_noise" onChange={onChange} checked={props.annotation.flag_ch_noise} disabled={!props.loggedIn} tooltip={tooltips.flag_ch_noise}>Channel noise</CheckboxField>
      <CheckboxField name="flag_line_noise" onChange={onChange} checked={props.annotation.flag_line_noise} disabled={!props.loggedIn} tooltip={tooltips.flag_line_noise}>Line noise</CheckboxField>
      </div>
      : null
      }

      <CheckboxField name="flag_other" onChange={onChange} checked={props.annotation.flag_other} disabled={!props.loggedIn} tooltip={tooltips.flag_other}>Other</CheckboxField>
      <CheckboxField name="flag_uncertain" onChange={onChange} checked={props.annotation.flag_uncertain} disabled={!props.loggedIn} tooltip={tooltips.flag_uncertain}>Uncertain</CheckboxField>
      <div className="flex mt-6 w-full">
        <label className="block w-full">
          <span className={"" + (props.loggedIn ? '' : 'opacity-50')}>Comments</span>
          <textarea className="block w-full mt-2" 
          onChange={props.onCommentFieldChange} defaultValue={props.annotation.comment} disabled={!props.loggedIn}/>
        </label>
      </div>
      <div className="flex mt-6">
        <Button onClick={props.onSubmit} disabled={!props.loggedIn}>Save </Button>
      </div>
    </form>
  )
}

export default AnnotationFormV2;