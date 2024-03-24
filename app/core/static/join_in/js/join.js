let dayInMillis = 24 * 60 * 60 * 1000;
$(".user-card").on("click", function () {
  let $userCard = $(this);
  $userCard.toggleClass("joined");
  $.ajax({
    type: "GET",
    url: `test_join_in/users/${$userCard.data("user-email")}`,
    success: function (data, textStatus, jqXHR) {
      let balanceElement = $userCard.find(".card-body .balance");
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

$(".submit-join-in-form").on("click", function () {
  let $submitButton = $(this);
  let $forTimestampInput = $("#for_timestamp_input");
  if ($submitButton.hasClass("for-today")) {
    $forTimestampInput.val('');
  } else {
    let currentTimestamp = parseInt($forTimestampInput.val());
    if ($submitButton.hasClass("day-before")) {
      $forTimestampInput.val(currentTimestamp - dayInMillis);
    } else if ($submitButton.hasClass("day-after")) {
      $forTimestampInput.val(currentTimestamp + dayInMillis);
    }
  }
  $("#join-in-form").trigger("submit");
});


$("#for_date").html(for_date.toDateString());