let dayInMillis = 24 * 60 * 60 * 1000;
$(".user-card").on("click", function () {
  let $userCard = $(this);
  $userCard.toggleClass("joined");
  $.ajax({
    type: "GET",
    url: `test_join_in/users/${$userCard.data("user-email")}`,
    success: function (data, textStatus, jqXHR) {
      // update user balance
      let $userBalanceElement = $userCard.find(".card-body .balance");
      let user_balance = Number(data.user.balance);
      $userBalanceElement.html(`€ ${user_balance.toFixed(2)}`);
      if (user_balance < 0) {
        $userBalanceElement.addClass("text-danger");
      } else {
        $userBalanceElement.removeClass("text-danger");
      }
      // update join_in balance
      let $balanceElement = $("#join_in_balance .balance");
      let balance = Number(data.join_in.balance);
      $balanceElement.html(`€ ${balance.toFixed(2)}`);
      if (balance < 0) {
        $balanceElement.addClass("text-danger");
      } else {
        $balanceElement.removeClass("text-danger");
      }
    },
    dataType: "json"
  });
});

$(".user-pay-link").on("click", function(event) {
  event.stopPropagation();
  let $userCard = $(this).closest('.user-card');
  let $userPayFormModal = $('#userPayFormModal');
  $userPayFormModal.find('#payment_user_name').html($userCard.data("user-email"));
  $userPayFormModal.find('#user-form-email').val($userCard.data("user-email"));
  $userPayFormModal.modal('show');
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

// $('#userPayFormModal').modal({ show: false});

$("#for_date").html(for_date.toDateString());