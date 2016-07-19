$(document).ready(function(){
  // for company_detail.html
  $('#testBtn').click(function () {
    var cnt=4;
    var btn = $(this);
    btn.button('loading');
    setTimeout(function () {
        cnt++;
        btn.button('reset');
        btn.text('  ' + cnt);
    }, 1000);
  });
  $('#testBtnDown').click(function () {
    var cnt=4;
    var btn = $(this);
    btn.button('loading');
    setTimeout(function () {
        if (cnt > 0) {
            cnt--;
        }
        btn.button('reset');
        btn.text('  ' + cnt);
    }, 1000);
  });
 // i18n.init(function(err, t) {
 //       $(".nav").i18n();
 //   });
 // for canvas_list.html
 vote = 'up'
 function thumbs(vote) {
    $('.glyphicon-thumbs-'+vote).click(function(){
        dom = $(this);
        id = dom.data("canvas-id");
        url = "/canvas/"+vote+"/" + id
        $.get(url, function(data) {
            dom.html(data[vote+'votes']);
            if(vote=='down'){
                opposite = 'up';
            }
            else{
                opposite = 'down';
            }
            if(opposite+'votes' in data){
                $('.glyphicon-thumbs-'+opposite+'[data-canvas-id="'+id+'"]').html(data[opposite+'votes']);
            }
        }).fail(function() {
            console.log( "failed to get " + url );
        });
    });
 }
 thumbs('up');
 thumbs('down');
});