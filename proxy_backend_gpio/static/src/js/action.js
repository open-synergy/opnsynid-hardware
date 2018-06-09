function proxy_backend_gpio_action(instance, module){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    module.ProxyBackendGPIO  = Backbone.Model.extend({

        initialize: function(attributes){
            return this;
        },

        get_proxy_backend: function(context){
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
                                self.send_action(proxy_ip, proxy_id, proxy_port, context);
                            }
                        )
                    }
                }
            );
        },

        send_action: function(proxy_ip, proxy_id, proxy_port, context){
            var self = this;
            var obj_proxy = new openerp.Model('proxy.backend');
            this.method_type = []
            this.channel = []
            this.mode = []
            this.interval = []
            console.log(context.context.mode);
            if (proxy_ip){
                this.proxy_url = "http://"+ proxy_ip + ":" + proxy_port
                this.proxy = new module.ProxyBackendDevice(this);
                this.proxy.connect(this.proxy_url);

                if (context.context.channel) this.channel = context.context.channel;
                if (context.context.mode) this.mode = context.context.mode;
                if (context.context.method_type) this.method_type = context.context.method_type;
                if (context.context.interval) this.interval = context.context.interval;

                if (this.method_type == "rpi_gpio_out_on"){
                    this.proxy.rpi_gpio_out_on(this.channel, this.mode);
                }
                else if (this.method_type == "rpi_gpio_out_off"){
                    this.proxy.rpi_gpio_out_off(this.channel, this.mode);
                }
                else if (this.method_type == "rpi_gpio_out_on_off_timer"){
                    this.proxy.rpi_gpio_out_on_off_timer(this.channel, this.mode, this.interval);
                }
                else {
                    console.log("No Method Type Defined");
                }
                
            }
        },

        action_gpio: function(context) {
            var self = this;
            self.get_proxy_backend(context);
            return true
        },
    });

    instance.web.client_actions.add('proxy_gpio', 'instance.proxy_backend_gpio.action');
    instance.proxy_backend_gpio.action = function (instance, context) {
        this.ProxyBackendGPIO = new module.ProxyBackendGPIO(this);
        if (context.context) {
            this.ProxyBackendGPIO.action_gpio(context);
        }
        else{
            console.log("No Context Defined")
        }
    };
};
