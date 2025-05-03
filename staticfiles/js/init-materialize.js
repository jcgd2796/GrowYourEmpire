document.addEventListener('DOMContentLoaded', function() {
    var tooltips = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltips);

    var sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    var tabs = document.querySelectorAll('.tabs');
    M.Tabs.init(tabs);

    var selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

    var textNeedCount = document.querySelectorAll('textarea');
    M.CharacterCounter.init(textNeedCount);

});
