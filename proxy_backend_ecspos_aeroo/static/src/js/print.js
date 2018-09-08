function proxy_backend_ecspos_aeroo_print(instance, module){
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.client_actions.add('print_aeroo_proxy', 'instance.proxy_backend_ecspos_aeroo.action');
    instance.proxy_backend_ecspos_aeroo.action = function (instance, context) {
        this.report_name = context.context.report_name;
        this.object_id = context.context.object_id;
        this.print_type = context.context.print_type;
        this.params = context.context.params || {};
        var parent = this;
        var obj_users = new openerp.Model('res.users');
        var obj_proxy = new openerp.Model('proxy.backend');
        var user_id = instance.session.uid
        obj_users.query(["name","proxy_backend_id"])
            .filter([['id', '=', user_id]])
            .first()
            .then(function (user) {
                if (user.proxy_backend_id){
                    parent.backend_id = user.proxy_backend_id[0]
                    parent.proxy = new openerp.proxy_backend.ProxyBackend(
                        this, parent.backend_id);
                    return parent.proxy.get_backend();
                }
            })
            .then(function(backend){
                if (backend != null){
                    if (parent.print_type == "continuous"){
                        obj_proxy.call('get_content_ecspos',[parent.report_name, parent.object_id, parent.params]).then(function(aeroo_content){
                            parent.proxy.print_receipt(aeroo_content, backend);
                        },function(err,event){
                            event.preventDefault();
                            console.log("Content should be Raw. Please try again.")
                        });
                    }
                    else{
                        for (var i = 0, len = parent.object_id.length; i<len; i++)
                        {   
                            obj_proxy.call('get_content_ecspos',[parent.report_name, [parent.object_id[i]]]).then(function(aeroo_content){
                                parent.proxy.print_receipt(aeroo_content, backend);
                            },function(err,event){
                                event.preventDefault();
                                console.log("Content should be Raw. Please try again.")
                            });
                        }
                    }
                }
                //TODO: Find more elegant way
                else{
                    alert("Failed to connect to proxy device");
                }
            })
    };    
};
