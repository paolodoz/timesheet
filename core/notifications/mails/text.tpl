Hi ${recipient_name},

% if notification_type == 'notify_new':
User ${submitter_name} ${submitter_surname} (${submitter_email}) has sent you an expence request for project ${project_name}.
% elif notification_type == 'notify_reject':
Your expence request for project ${project_name} has been rejected by ${approver_name} ${approver_surname} (${approver_email}).
% elif notification_type == 'notify_approve':
Your expence request for project ${project_name} has been approved by ${approver_name} ${approver_surname} (${approver_email})!
% endif

Expence data:

Project: ${project_name}
Expence type: ${expence_type}
% if expence_objects:
Amount: ${ sum(o.get('amount',0) for o in expence_objects) }
% endif
Approver user: ${approver_name} ${approver_surname} (${approver_email})
Requesting user: ${submitter_name} ${submitter_surname} (${submitter_email})
Date: ${expence_date}
% if expence_notes:
Notes: 
	% for note in expence_notes:
  - ${note}
	% endfor
% endif





