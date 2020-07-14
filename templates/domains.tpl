% include('header.tpl', title='SSL checker dashboard')


<table>
<caption><strong>SSL Certificate Expiration, Days</strong></caption>
<tr><th>Domain/Hostname</th><th>Days befor expiration</th></tr>
%for row in rows:
    <tr>
    %i = 0
    %for col in row:
        %i += 1
        <td>
        %if i == 2:
            %if not isinstance(col, int) or col < 10:
                <span class="_{{i}} red">
            %elif col < 60:
                <span class="_{{i}} yellow">
            %elif col < 90:
                <span class="_{{i}} green">
            %else:
                <span class="_{{i}} default">
            %end
            {{col}}
        %end
        %if i == 1:
            <a href="https://{{col}}">{{col}}</a>
        %end
        </span></td>
    %end
    </tr>
%end
</table>

%end

% include('footer.tpl')