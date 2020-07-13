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
            %if isinstance(col, int) and col < 10 or not isinstance(col, int):
                <span class="_{{i}} red">
            %elif isinstance(col, int) and col < 60:
                <span class="_{{i}} yellow">
            %elif isinstance(col, int) and col < 90:
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