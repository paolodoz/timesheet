Dear ${recipient_name} ${recipient_surname},

Your expence request has been rejected.

Expence data:

Type: ${expence_type}
Requesting user: ${submitter_name} ${submitter_surname} (${submitter_email})
Date: ${expence_date}
% if expence_objects:
Amount: ${ sum(o.get('amount',0) for o in expence_objects) }
% endif
% if expence_notes:
Notes: 
	% for note in expence_notes:
- ${note}
	% endfor
% endif