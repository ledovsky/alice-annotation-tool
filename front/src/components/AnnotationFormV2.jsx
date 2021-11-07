/*
Here we implement the methodology specified in the documentation
*/

import { React } from 'react';
import { useState } from 'react';

import Button from '../common/Button';
import CheckboxField from '../common/CheckboxField';


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
      upd = {...upd, "eyes_blinks": false, "flag_eyes_h": false, "flag_eyes_v": false};
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
      <CheckboxField name="flag_brain" onChange={onChange} checked={props.annotation.flag_brain} disabled={!props.loggedIn}>Brain</CheckboxField>
      { props.annotation.flag_brain ?
      <div className="ml-10">
        <CheckboxField name="flag_mu" onChange={onChange} checked={props.annotation.flag_mu} disabled={!props.loggedIn}>Mu rhythm</CheckboxField>
        <CheckboxField name="flag_alpha" onChange={onChange} checked={props.annotation.flag_alpha} disabled={!props.loggedIn}>Alpha rhythm</CheckboxField>
      </div>
      : null
      }

      {/* Eyes block */}
      <CheckboxField name="flag_eyes" onChange={onChange} checked={props.annotation.flag_eyes} disabled={!props.loggedIn}>Eyes</CheckboxField>
      { props.annotation.flag_eyes ?
      <div className="ml-10">
      <CheckboxField name="flag_eyes_blinks" onChange={onChange} checked={props.annotation.flag_eyes_blinks} disabled={!props.loggedIn}>Eye Blinks</CheckboxField>
      <CheckboxField name="flag_eyes_h" onChange={onChange} checked={props.annotation.flag_eyes_h} disabled={!props.loggedIn}>Eyes Horizontal</CheckboxField>
      <CheckboxField name="flag_eyes_v" onChange={onChange} checked={props.annotation.flag_eyes_v} disabled={!props.loggedIn}>Eyes Vertical</CheckboxField>
      </div>
      : null
      }

      {/* Muscle and Movement block */}
      <CheckboxField name="flag_muscles_and_movement" onChange={onChange} checked={props.annotation.flag_muscles_and_movement} disabled={!props.loggedIn}>Muscles and Movement</CheckboxField>
      { props.annotation.flag_muscles_and_movement ?
      <div className="ml-10">
      <CheckboxField name="flag_muscles" onChange={onChange} checked={props.annotation.flag_muscles} disabled={!props.loggedIn}>Muscles</CheckboxField>
      <CheckboxField name="flag_movement" onChange={onChange} checked={props.annotation.flag_movement} disabled={!props.loggedIn}>Movement</CheckboxField>
      </div>
      : null
      }

      <CheckboxField name="flag_heart" onChange={onChange} checked={props.annotation.flag_heart} disabled={!props.loggedIn}>Heart</CheckboxField>

      {/* Noise block */}
      <CheckboxField name="flag_noise" onChange={onChange} checked={props.annotation.flag_noise} disabled={!props.loggedIn}>Noise</CheckboxField>
      { props.annotation.flag_noise ?
      <div className="ml-10">
      <CheckboxField name="flag_ch_noise" onChange={onChange} checked={props.annotation.flag_ch_noise} disabled={!props.loggedIn}>Channel noise</CheckboxField>
      <CheckboxField name="flag_line_noise" onChange={onChange} checked={props.annotation.flag_line_noise} disabled={!props.loggedIn}>Line noise</CheckboxField>
      </div>
      : null
      }

      <CheckboxField name="flag_other" onChange={onChange} checked={props.annotation.flag_other} disabled={!props.loggedIn}>Other</CheckboxField>
      <CheckboxField name="flag_uncertain" onChange={onChange} checked={props.annotation.flag_uncertain} disabled={!props.loggedIn}>Uncertain</CheckboxField>
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