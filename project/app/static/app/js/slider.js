$(document).ready(function(){
    $('#carouselExample').on('slide.bs.carousel', function (e) {
      var $e = $(e.relatedTarget);
      $e.addClass('active');
      setTimeout(function () {
        $e.removeClass('active');
      }, 1000);
    });

    $('#carouselExample').carousel({
      interval: 3000, // Intervalle de temps en millisecondes pour la transition automatique
      pause: "false"
    });
  });