% include('header.tpl', title='SSL checker dashboard')


<table>
<caption><strong>SSL Certificate Expiration, Days</strong></caption>
<tr><th>#</th><th>Domain/Hostname</th><th>Days befor expiration</th></tr>
%i = 0
%for domain in sorted(domains_days):
    <tr>
    %for column in [0, 1, 2]:
        <td>
        %if column == 0:
            %i += 1
            {{i}}
        %end
        %if column == 1:
            <a href="https://{{domain}}">{{domain}}</a>
        %end
        %if column == 2:
            %days = domains_days[domain]
            %if not isinstance(days, int) or days < 30:
                <span class="_{{column}} red">
            %elif days < 60:
                <span class="_{{column}} yellow">
            %elif days < 90:
                <span class="_{{column}} green">
            %else:
                <span class="_{{column}} default">
            %end
            {{days}}
        %end
            </span>
        </td>
    %end
    </tr>
%end
</table>

%end

% include('footer.tpl')