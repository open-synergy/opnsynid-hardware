function proxy_backend_ecspos_aeroo_print(instance, module){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    module.PrintAerooProxy  = Backbone.Model.extend({

        initialize: function(attributes){
            return this;
        },

        get_template: function(report_name, object_id){
            var self = this;
            var obj_users = new openerp.Model('res.users');
            var obj_proxy = new openerp.Model('proxy.backend');
            var user_id = instance.session.uid
            obj_users.query(["name","proxy_backend_id"])
                .filter([['id', '=', user_id]])
                .first()
                .then(function (user) {
                    if (user.proxy_backend_id){
                        proxy_id = user.proxy_backend_id[0]
                        obj_proxy.query(["backend_ip", "port"])
                            .filter([['id', '=', proxy_id]])
                            .first()
                            .then(function (proxy) {
                                proxy_ip = proxy.backend_ip
                                proxy_port = proxy.port
                                proxy_id = proxy.id
                                self.call_template(proxy_ip, proxy_id, proxy_port, report_name, object_id);
                            }
                        )
                    }
                }
            );
        },

        call_template: function(proxy_ip, proxy_id, proxy_port, report_name, object_id){
            var self = this;
            var obj_proxy = new openerp.Model('proxy.backend');
            if (proxy_ip){
                this.proxy_url = "http://"+ proxy_ip + ":" + proxy_port
                this.proxy = new module.ProxyBackendDevice(this);
                this.proxy.connect(this.proxy_url)
                obj_proxy.call('get_content_ecspos',[report_name, object_id]).then(function(aeroo_content){
                    self.proxy.print_receipt(aeroo_content);
                },function(err,event){
                    event.preventDefault();
                    console.log("Content should be Raw. Please try again.")
                });
            }
        },

        print_report_aeroo: function(report_name, object_id) {
            var self = this;
            self.get_template(report_name, object_id);
            return true
        },
    });

    instance.web.client_actions.add('print_aeroo_proxy', 'instance.proxy_backend_ecspos_aeroo.action');
    instance.proxy_backend_ecspos_aeroo.action = function (instance, context) {
        this.report_name = []
        this.object_id = []
        this.PrintAerooProxy = new module.PrintAerooProxy(this);
        if (context.context.report_name) this.report_name = context.context.report_name;
        if (context.context.object_id) this.object_id = context.context.object_id;
        if (this.report_name && this.object_id) {
            this.PrintAerooProxy.print_report_aeroo(this.report_name, this.object_id);
        }
        else{
            console.log("No Context Defined")
        }
    };
};
