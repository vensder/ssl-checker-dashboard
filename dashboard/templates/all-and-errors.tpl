% include('header.tpl', title='SSL checker dashboard')


<table class="inlineTable">
<caption><strong>SSL Certificate Expiration, Days</strong></caption>
<tr><th>#</th><th>Hostname</th><th>Days befor expiration</th><th>Last info update</th></tr>
%i = 0
%for host in hosts_good:
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
            %days = hosts_good[host][0]
            %if not isinstance(days, int) or days < 30:
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
            {{hosts_good[host][1]}}
        %end
        </td>
    %end
    </tr>
%end
</table>

<table class="inlineTable">
    <caption><strong>SSL Certificates Errors</strong></caption>
    <tr><th>#</th><th>Hostname</th><th>Errors</th><th>Last info update</th></tr>
    %i = 0
    %for host in hosts_bad:
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
                <span class="_{{column}} red">
                <a href="/{{host}}">{{hosts_bad[host][0]}}</a>
                </span>
            %end
            %if column == 3:
                {{hosts_bad[host][1]}}
            %end
            </td>
        %end
        </tr>
    %end
    </table>

%end

% include('footer.tpl')