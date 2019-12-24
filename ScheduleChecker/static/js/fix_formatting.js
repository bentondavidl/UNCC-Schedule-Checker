

function fix_time(datetime) {
    var time = datetime.split(' ')[1];
    var hours = time.split(':')[0];
    var minutes = time.split(':')[1];
    var ampm = hours >= 12 ? 'pm' : 'am';

    hours = hours % 12;
    hours = hours ? hours : 12;

    document.write(hours + ':' + minutes + ' ' + ampm);
}

function resolve_day(day) {
    switch(day) {
        case 'M' : document.write('Monday'); break;
        case 'T' : document.write('Tuesday'); break;
        case 'W' : document.write('Wednesday'); break;
        case 'R' : document.write('Thursday'); break;
        case 'F' : document.write('Friday'); break;
    }
}