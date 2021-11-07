import { React } from 'react';

import Button from '../common/Button';
import CheckboxField from '../common/CheckboxField';


function AnnotationForm( props ) {
  return (
    <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <div className="flex">
        <p className="font-bold">Select IC classes</p>
      </div>
      <CheckboxField name="flag_brain" onChange={props.onChange} checked={props.annotation.flag_brain} disabled={!props.loggedIn}>Brain</CheckboxField>
      <CheckboxField name="flag_mu" onChange={props.onChange} checked={props.annotation.flag_mu} disabled={!props.loggedIn}>Mu rhythm</CheckboxField>
      <CheckboxField name="flag_alpha" onChange={props.onChange} checked={props.annotation.flag_alpha} disabled={!props.loggedIn}>Alpha rhythm</CheckboxField>
      <CheckboxField name="flag_eyes" onChange={props.onChange} checked={props.annotation.flag_eyes} disabled={!props.loggedIn}>Eyes</CheckboxField>
      <CheckboxField name="flag_eyes_h" onChange={props.onChange} checked={props.annotation.flag_eyes_h} disabled={!props.loggedIn}>Eyes Horizontal</CheckboxField>
      <CheckboxField name="flag_eyes_v" onChange={props.onChange} checked={props.annotation.flag_eyes_v} disabled={!props.loggedIn}>Eyes Vertical</CheckboxField>
      <CheckboxField name="flag_muscles" onChange={props.onChange} checked={props.annotation.flag_muscles} disabled={!props.loggedIn}>Muscles</CheckboxField>
      <CheckboxField name="flag_heart" onChange={props.onChange} checked={props.annotation.flag_heart} disabled={!props.loggedIn}>Heart</CheckboxField>
      <CheckboxField name="flag_ch_noise" onChange={props.onChange} checked={props.annotation.flag_ch_noise} disabled={!props.loggedIn}>Channel noise</CheckboxField>
      <CheckboxField name="flag_line_noise" onChange={props.onChange} checked={props.annotation.flag_line_noise} disabled={!props.loggedIn}>Line noise</CheckboxField>
      <CheckboxField name="flag_other" onChange={props.onChange} checked={props.annotation.flag_other} disabled={!props.loggedIn}>Other</CheckboxField>
      <CheckboxField name="flag_uncertain" onChange={props.onChange} checked={props.annotation.flag_uncertain} disabled={!props.loggedIn}>Uncertain</CheckboxField>
      <div className="flex mt-6 w-full">
        <label className="block w-full">
          <span className={"" + (props.loggedIn ? '' : 'opacity-50')}>Comments</span>
          <textarea className="block w-full mt-2" onChange={props.onCommentFieldChange} defaultValue={props.annotation.comment} disabled={!props.loggedIn}/>
        </label>
      </div>
      <div className="flex mt-6">
        <Button onClick={props.onSubmit} disabled={!props.loggedIn}>Save</Button>
      </div>
    </form>
  )
}

export default AnnotationForm;