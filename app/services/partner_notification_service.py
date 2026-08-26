# from app.repositories.partner_notification_repository import (
#     PartnerNotificationRepository,
# )


# class PartnerNotificationService:

#     @staticmethod
#     def get_notifications(
#         staff_email: str,
#     ):
#         return PartnerNotificationRepository.get_notifications(
#             staff_email=staff_email,
#         )

#     @staticmethod
#     def mark_as_read(
#         notification_id: str,
#         staff_email: str,
#     ):
#         data = (
#             PartnerNotificationRepository.mark_as_read(
#                 notification_id=notification_id,
#                 staff_email=staff_email,
#             )
#         )

#         return {
#             "success": True,
#             "data": data,
#         }

#     @staticmethod
#     def delete_notification(
#         notification_id: str,
#         staff_email: str,
#     ):
#         (
#             PartnerNotificationRepository.delete_notification(
#                 notification_id=notification_id,
#                 staff_email=staff_email,
#             )
#         )

#         return {
#             "success": True,
#             "message": "Notification deleted successfully.",
#         }

#     @staticmethod
#     def delete_all_notifications(
#         staff_email: str,
#     ):
#         (
#             PartnerNotificationRepository.delete_all_notifications(
#                 staff_email=staff_email,
#             )
#         )

#         return {
#             "success": True,
#             "message": "All notifications deleted successfully.",
#         }

















from app.repositories.partner_notification_repository import (
    PartnerNotificationRepository,
)

from app.services.notification_service import (
    NotificationService,
)


class PartnerNotificationService:

    @staticmethod
    def get_notifications(
        staff_email: str,
    ):
        return PartnerNotificationRepository.get_notifications(
            staff_email=staff_email,
        )

    @staticmethod
    def mark_as_read(
        notification_id: str,
        staff_email: str,
    ):
        data = (
            PartnerNotificationRepository.mark_as_read(
                notification_id=notification_id,
                staff_email=staff_email,
            )
        )

        return {
            "success": True,
            "data": data,
        }

    @staticmethod
    def delete_notification(
        notification_id: str,
        staff_email: str,
    ):
        PartnerNotificationRepository.delete_notification(
            notification_id=notification_id,
            staff_email=staff_email,
        )

        return {
            "success": True,
            "message": "Notification deleted successfully.",
        }

    @staticmethod
    def delete_all_notifications(
        staff_email: str,
    ):
        PartnerNotificationRepository.delete_all_notifications(
            staff_email=staff_email,
        )

        return {
            "success": True,
            "message": "All notifications deleted successfully.",
        }

    # =========================================================
    # SEND STAFF NOTIFICATION
    # =========================================================

    @staticmethod
    async def send_staff_notification(
        email: str,
        title: str | None = None,
        body: str | None = None,
        data: dict | None = None,
    ):
        return await NotificationService.send_to_staff_email(
            email=email,
            title=title,
            body=body,
            data=data,
        )

    # =========================================================
    # SEND DIRECTLY TO TOKEN
    # =========================================================

    @staticmethod
    async def send_to_token(
        token: str,
        title: str | None = None,
        body: str | None = None,
        data: dict | None = None,
    ):
        return await NotificationService.send_to_token(
            token=token,
            title=title,
            body=body,
            data=data,
        )