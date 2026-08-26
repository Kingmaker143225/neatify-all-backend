from app.repositories.referral_milestone_repository import (
    ReferralMilestoneRepository,
)

from app.services.notification_service import (
    NotificationService,
)


class ReferralMilestoneService:

    # =========================================================
    # CHECK ALL REFERRAL MILESTONES
    # =========================================================

    @staticmethod
    async def check_milestones():

        notified_count = 0
        skipped_count = 0
        errors_count = 0

        # =====================================================
        # 1. 30-BOOKING REFERRAL MILESTONES
        # =====================================================

        milestones = (
            ReferralMilestoneRepository
            .get_pending_30_booking_milestones()
        )

        for item in milestones:

            try:
                referral_id = str(item["id"])
                referral_code = item.get("referral_code")
                full_name = item.get("full_name") or "your referral"

                if not referral_code:
                    skipped_count += 1
                    continue

                # -------------------------------------------------
                # Find referrer
                # -------------------------------------------------

                profile = (
                    ReferralMilestoneRepository
                    .get_referrer_by_code(referral_code)
                )

                if not profile:
                    skipped_count += 1

                    print(
                        f"⚠️ Referrer not found for referral "
                        f"{full_name}"
                    )

                    continue

                push_token = profile.get("push_token")
                staff_email = profile.get("email")

                # -------------------------------------------------
                # No push token
                #
                # IMPORTANT:
                # Do NOT mark notification as sent.
                # The next job should retry.
                # -------------------------------------------------

                if not push_token:

                    skipped_count += 1

                    print(
                        f"⚠️ No push token for referrer "
                        f"{staff_email}. Will retry later."
                    )

                    continue

                # -------------------------------------------------
                # Store in notifications table
                # -------------------------------------------------

                notification_data = {
                    "staff_email": staff_email,
                    "title": "Referral Reward Earned 🎉",
                    "body": (
                        f"Congratulations! Your referral "
                        f"{full_name} has successfully completed "
                        f"30 bookings. You have earned a referral "
                        f"reward of ₹1,500 which will be credited "
                        f"shortly."
                    ),
                    "type": "referral_reward",
                    "is_read": False,
                    "booking_id": None,
                }

                (
                    ReferralMilestoneRepository
                    .create_notification(
                        notification_data
                    )
                )

                # -------------------------------------------------
                # Send push notification
                # -------------------------------------------------

                result = await NotificationService.send_to_token(
                    token=push_token,
                    title="Referral Milestone Reached! 🎉",
                    body=(
                        f"Congratulations! Your referred person, "
                        f"{full_name}, has successfully completed "
                        f"30 bookings. You have earned a reward "
                        f"of ₹1500, which you will receive shortly."
                    ),
                    data={
                        "screen": "new-services",
                        "type": "referral_bonus_unlocked",
                        "referral_id": referral_id,
                    },
                )

                # -------------------------------------------------
                # Mark as sent ONLY after push succeeds
                # -------------------------------------------------

                (
                    ReferralMilestoneRepository
                    .mark_bonus_notification_sent(
                        referral_id
                    )
                )

                notified_count += 1

                print(
                    f"✅ 30-booking referral notification sent "
                    f"for {full_name}"
                )

            except Exception as error:

                errors_count += 1

                print(
                    "❌ 30-booking referral notification error:",
                    str(error),
                )

        # =====================================================
        # 2. REFERRAL REWARD PAID
        # =====================================================

        paid_rewards = (
            ReferralMilestoneRepository
            .get_pending_paid_rewards()
        )

        for item in paid_rewards:

            try:
                referral_id = str(item["id"])
                referral_code = item.get("referral_code")
                full_name = item.get("full_name") or "your referral"

                if not referral_code:
                    skipped_count += 1
                    continue

                # -------------------------------------------------
                # Find referrer
                # -------------------------------------------------

                profile = (
                    ReferralMilestoneRepository
                    .get_referrer_by_code(referral_code)
                )

                if not profile:
                    skipped_count += 1
                    continue

                push_token = profile.get("push_token")
                staff_email = profile.get("email")

                # -------------------------------------------------
                # Store notification
                # -------------------------------------------------

                notification_data = {
                    "staff_email": staff_email,
                    "title": "Referral Reward Credited 💰",
                    "body": (
                        f"Your referral reward amount of ₹1,500 "
                        f"for {full_name} has been credited "
                        f"successfully."
                    ),
                    "type": "referral_reward_paid",
                    "is_read": False,
                    "booking_id": None,
                }

                (
                    ReferralMilestoneRepository
                    .create_notification(
                        notification_data
                    )
                )

                # -------------------------------------------------
                # Send push if token exists
                # -------------------------------------------------

                if push_token:

                    await NotificationService.send_to_token(
                        token=push_token,
                        title="Referral Reward Credited 💰",
                        body=(
                            f"Your referral reward amount of "
                            f"₹1,500 for {full_name} has been "
                            f"credited successfully."
                        ),
                        data={
                            "screen": "new-services",
                            "type": "referral_reward_paid",
                            "referral_id": referral_id,
                        },
                    )

                # -------------------------------------------------
                # Mark as sent
                # -------------------------------------------------

                (
                    ReferralMilestoneRepository
                    .mark_reward_paid_notification_sent(
                        referral_id
                    )
                )

                notified_count += 1

                print(
                    f"✅ Referral reward paid notification "
                    f"processed for {full_name}"
                )

            except Exception as error:

                errors_count += 1

                print(
                    "❌ Referral reward paid notification error:",
                    str(error),
                )

        # =====================================================
        # RESULT
        # =====================================================

        result = {
            "success": True,
            "notified_count": notified_count,
            "skipped_count": skipped_count,
            "errors_count": errors_count,
        }

        print(
            "🏁 REFERRAL MILESTONE JOB FINISHED:",
            result,
        )

        return result