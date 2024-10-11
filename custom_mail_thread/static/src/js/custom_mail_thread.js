odoo.define('custom_mail_thread.custom_mail_thread', function (require) {
    "use strict";

    const { registerInstancePatchModel } = require('mail/static/src/model/model_core.js');

    registerInstancePatchModel('mail.thread', 'custom_mail_thread/static/src/js/custom_mail_thread.js', {
        async refreshActivities() {
            if (!this.hasActivities) {
                return;
            }
            if (this.isTemporary) {
                return;
            }

            const recordData = await this.async(() => this.env.services.rpc({
                model: this.model,
                method: 'search',
                args: [[['id', '=', this.id]]],
                kwargs: {
                    context: { active_test: false },
                },
            }, { shadow: true }));

            if (recordData.length === 0) {
                return
            }
            // A bit "extreme", may be improved
            const [{ activity_ids: newActivityIds }] = await this.async(() => this.env.services.rpc({
                model: this.model,
                method: 'read',
                args: [this.id, ['activity_ids']]
            }, { shadow: true }));
            const activitiesData = await this.async(() => this.env.services.rpc({
                model: 'mail.activity',
                method: 'activity_format',
                args: [newActivityIds]
            }, { shadow: true }));
            const activities = this.env.models['mail.activity'].insert(activitiesData.map(
                activityData => this.env.models['mail.activity'].convertData(activityData)
            ));
            this.update({ activities: [['replace', activities]] });
        },

        async refreshFollowers() {
            if (this.isTemporary) {
                this.update({ followers: [['unlink-all']] });
                return;
            }
            try {
                const response = await this.async(() => this.env.services.rpc({
                    route: '/mail/read_followers',
                    params: {
                        res_id: this.id,
                        res_model: this.model,
                    },
                }, { shadow: true }));

                this.update({ areFollowersLoaded: true });
                if (response.followers.length > 0) {
                    this.update({
                        followers: [['insert-and-replace', response.followers.map(data =>
                            this.env.models['mail.follower'].convertData(data))
                        ]],
                    });
                } else {
                    this.update({
                        followers: [['unlink-all']],
                    });
                }
            } catch (e) {
                this.update({ followers: [['unlink-all']] });
                return;
            }
        }
    });



});

