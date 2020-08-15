% include('header.tpl', title='SSL checker dashboard')


<table>
<caption><strong>{{table_caption}}</strong></caption>
<tr><th>#</th><th>Hostname</th><th>{{table_header}}</th><th>Last info update</th></tr>
%i = 0
%for host in hosts_days:
    <tr>
    %for column in [0, 1, 2, 3]:
        <td>
        %if column == 0:
            %i += 1
            {{i}}
        %end
        %if column == 1:
            <a href="https://{{host}}">{{host}}</a>
        %end
        %if column == 2:
            %days = hosts_days[host][0]
            %if not isinstance(days, int):
                <span class="_{{column}} red">
            %elif days < 30:
                <span class="_{{column}} pink">
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
        %if column == 3:
            {{hosts_days[host][1]}}
        %end
        </td>
    %end
    </tr>
%end
</table>

%end

% include('footer.tpl')