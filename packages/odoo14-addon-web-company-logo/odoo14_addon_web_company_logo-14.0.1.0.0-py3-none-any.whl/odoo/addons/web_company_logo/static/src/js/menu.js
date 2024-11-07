odoo.define('web_company_logo.web_company_logo', function (require) {
    "use strict";

    var session = require('web.session');
    var Menu = require('web.SystrayMenu');

    Menu.include({
        /**
         * @override
         */
        start: function (parent, options) {
            this._super.apply(this, arguments);

            var url = window.location.origin;
            var companyId = session.company_id;
            $.ajax({
                type: 'GET',
                data: {'company_id': companyId},
                url: `${url}/check_company_logo`,
                success: function (result) {
                    var result = JSON.parse(result);
                    if (result.has_logo == true) {
                        $('#company-logo')[0].src = `${url}/web/image?model=res.company&id=${companyId}&field=logo`;
                    }
                    else {
                        $('#company-logo-link')[0].remove();
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log('Error encountered');
                },
            });
        }
    })
    return Menu;
});
