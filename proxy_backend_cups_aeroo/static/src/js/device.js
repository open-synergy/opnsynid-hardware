function proxy_backend_cups_aeroo_device(instance, module){
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var _super = module.ProxyBackend;
    module.ProxyBackend = module.ProxyBackend.extend({
        print_using_cups: function(receipt, backend, printer_name){
            var self = this;
            if(receipt){
                this.receipt_queue.push(receipt);
            }
            var aborted = false;
            function send_printing_job(){
                if (self.receipt_queue.length > 0){
                    var r = self.receipt_queue.shift();
                    self.message_json(backend, "POST", "print_using_cups", {"data": r, "printer_name": printer_name})
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

