% include('header.tpl', title='SSL checker dashboard')


<table>
<caption><strong>SSL Certificate Expiration, Days</strong></caption>
<tr><th>Domain/Hostname</th><th>Days befor expiration</th></tr>
%for domain in sorted(domains_days):
    <tr>
    %for i in [1, 2]:
        <td>
        %if i == 1:
            <a href="https://{{domain}}">{{domain}}</a>
        %end
        %if i == 2:
            %days = domains_days[domain]
            %if not isinstance(days, int) or days < 30:
                <span class="_{{i}} red">
            %elif days < 60:
                <span class="_{{i}} yellow">
            %elif days < 90:
                <span class="_{{i}} green">
            %else:
                <span class="_{{i}} default">
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