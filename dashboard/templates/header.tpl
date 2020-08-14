<!doctype html>

<html lang="en">

<head>
    <meta charset="utf-8">

    <title>{{title}}</title>
    <meta name="description" content="SSL certs status page for subhost list">
    <link rel="stylesheet" href="static/styles.css?v=1.0">
    %if refresh:
    <script type="text/javascript">
        page_refresh = window.setTimeout(
            function () {
                window.location.href = window.location.href
            },
            {{ refresh }}* 2000);
    </script>

    <noscript>
        <meta http-equiv="refresh" content="{{refresh}}" />
    </noscript>
    %end
</head>

<body>
    <header>
        <p>
            <a href="/all"> All</a>
            | <a href="/good"> Good</a>
            | <a href="/bad"> Bad</a>
            | <a href="/health"> Health</a>
            | Running on: {{ hostname }}
            | Redis available: {{ redis_available }}
            | Hosts in Redis cache: {{ hosts_in_redis }}
            | Hosts in dashboard cache: {{ hosts_in_dashboard_cache }}
        </p>
    </header>
