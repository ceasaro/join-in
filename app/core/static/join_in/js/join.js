$(".user-card").on("click", function () {
  var $userCard = $(this);
  $userCard.toggleClass("joined",
    function (index, currentclass) {
      debugger;
    }
  );
  console.info($userCard.data("user-email"));
  $.ajax({
    type: "GET",
    url: `test_join_in/users/${$userCard.data("user-email")}`,
    success:  function(data, textStatus, jqXHR ) {
      let balanceElement = $userCard.find('.card-body .balance');
      let balance = Number(data.user.balance);
      balanceElement.html(`€ ${balance.toFixed(2)}`);
      if (balance < 0) {
        balanceElement.addClass("text-danger");
      } else {
        balanceElement.removeClass("text-danger");
      }
    },
    dataType: "json"
  });
});
