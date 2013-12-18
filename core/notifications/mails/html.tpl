<html>

<p>
Hi ${recipient_name},
</p>

<p>
% if notification_type == 'notify_new':
User ${submitter_name} ${submitter_surname} (${submitter_email}) has sent you an expence request for project ${project_name}.
% elif notification_type == 'notify_reject':
Your expence request for project ${project_name} has been rejected by ${approver_name} ${approver_surname} (${approver_email}).
% elif notification_type == 'notify_approve':
Your expence request for project ${project_name} has been approved by ${approver_name} ${approver_surname} (${approver_email})!
% endif
</p>

<p>

<table border="0">
  <thead>
    <tr>
% for header in ('project', 'type', 'amount', 'approver', 'applicant', 'expence date', 'notes'):
      <td>${header}</td>
% endfor
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>${project_name}</td>
      <td>${expence_type}</td>
      <td>${ sum(o.get('amount',0) for o in expence_objects) }</td>
      <td>${approver_email}</td>
      <td>${submitter_email}</td>
      <td>${expence_date}</td>
      <td>${ '<br/>'.join(expence_notes) }</td>
    </tr>
  </tbody>
</table>

</p>

</html>



