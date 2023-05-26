import React from 'react';
import AnnotationBar from './AnnotationBar';
import Check from '../common/Check';
import moment from 'moment';


function AnnotationList (props) {
  const rows = props.annotations.map((a) =>
    <tr key={a.id.toString()}>
      <td className="border px-4 py-2">{a.user.first_name} {a.user.last_name}</td>
      <td className="border px-4 py-2">{ moment(a.updated_at).format('YYYY-MM-DD h:mm') }</td>
      <td className="border px-4 py-2"> <Check flag={a.flag_brain} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_mu} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_alpha} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_eyes} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_eyes_v} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_eyes_h} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_muscles} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_heart} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_line_noise} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_ch_noise} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_uncertain} /> </td>
      <td className="border px-4 py-2"> <Check flag={a.flag_other} /> </td>
    </tr>
  );
  // const rows = []
  return (
    <React.Fragment>
      <AnnotationBar ic={props.ic} dataset={props.dataset} state="list"/>
      <div className="ml-6">
        <p className="text-4xl">ICs </p>
        <table className="table-auto">
          <thead>
            <tr>
              <th className="px-4 py-2">User</th>
              <th className="px-4 py-2">Updated</th>
              <th className="px-4 py-2">Brain</th>
              <th className="px-4 py-2">Mu</th>
              <th className="px-4 py-2">Alpha</th>
              <th className="px-4 py-2">Eyes</th>
              <th className="px-4 py-2">Eyes Vert</th>
              <th className="px-4 py-2">Eyes Hor</th>
              <th className="px-4 py-2">Muscles</th>
              <th className="px-4 py-2">Heart</th>
              <th className="px-4 py-2">Line Noise</th>
              <th className="px-4 py-2">Ch Noise</th>
              <th className="px-4 py-2">Uncert</th>
              <th className="px-4 py-2">Other</th>
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </React.Fragment>
  )
}

export default AnnotationList;