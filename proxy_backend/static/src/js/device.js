function proxy_device(instance,module){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    module.ProxyBackendDevice  = instance.web.Class.extend(openerp.PropertiesMixin,{
        init: function(parent,options){
            openerp.PropertiesMixin.init.call(this,parent);
            var self = this;
            options = options || {};
            url = options.url || 'http://localhost:8069';

            this.receipt_queue = [];

            this.notifications = {};
            this.bypass_proxy = false;

            this.connection = null;
            this.host       = '';
            this.keptalive  = false;

            this.set('status',{});

            this.set_connection_status('disconnected');

            window.hw_proxy = this;
        },
        set_connection_status: function(status,drivers){
            oldstatus = this.get('status');
            newstatus = {};
            newstatus.status = status;
            newstatus.drivers = status === 'disconnected' ? {} : oldstatus.drivers;
            newstatus.drivers = drivers ? drivers : newstatus.drivers;
            this.set('status',newstatus);
        },
        disconnect: function(){
            if(this.get('status').status !== 'disconnected'){
                this.connection.destroy();
                this.set_connection_status('disconnected');
            }
        },

        connect: function(url){
            var self = this;
            this.connection = new instance.web.Session(undefined,url, { use_cors: true});
            this.host   = url;
            this.set_connection_status('connecting',{});

            return this.message('handshake').then(function(response){
                    if(response){
                        self.set_connection_status('connected');
                        localStorage['hw_proxy_url'] = url;
                        console.log('Connected');
                    }else{
                        self.set_connection_status('disconnected');
                        console.error('Connection refused by the Proxy');
                    }
                },function(){
                    self.set_connection_status('disconnected');
                    console.error('Could not connect to the Proxy');
                });
        },
        message : function(name,params){
            var callbacks = this.notifications[name] || [];
            for(var i = 0; i < callbacks.length; i++){
                callbacks[i](params);
            }

            if(this.get('status').status !== 'disconnected'){
                return this.connection.rpc('/hw_proxy/' + name, params || {});
            }else{
                return (new $.Deferred()).reject();
            }
        },

        log: function(){
            return this.message('log',{'arguments': _.toArray(arguments)});
        },

    });
};
