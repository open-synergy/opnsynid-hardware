function proxy_backend_ecspos_aeroo_print_device(instance, module){
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var _super = module.ProxyBackend;
    module.ProxyBackend = module.ProxyBackend.extend({
        print_receipt: function(receipt, backend){
            var self = this;
            if(receipt){
                this.receipt_queue.push(receipt);
            }
            var aborted = false;
            function send_printing_job(){
                if (self.receipt_queue.length > 0){
                    var r = self.receipt_queue.shift();
                    self.message_json(backend, "POST", "print_xml_receipt", {"receipt": r})
                        .then(function(){
                            send_printing_job();
                        },function(error){
                            if (error) {
                                console.log("Error when printing")
                                return;
                            }
                            self.receipt_queue.unshift(r)
                        });
                }
            }
            send_printing_job();
        },
    });
};
