/**
 * Slider Pagination Concept
 * jquery.pagination.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2012, Codrops
 * http://www.codrops.com
 */
;(function($, window, undefined) {
    'use strict';

    $.Slider = function(settings, element) {
        this.$el = element;
        this.value = settings.value;
        this.total = settings.total;
        this.width = settings.width;
        this._create();
    };
    $.Slider.prototype = {
        _create: function() {
            var self = this;
            this.slider = this.$el.slider( {
                value: this.value,
                min: 1,
                max: this.total,
                step: 1
            } );
            this.$value = $('<span>' + this.value + '</span>');
            this.getHandle().append(this.$value);
        },
        setValue: function(value) {
            this.value = value;
            this.$value.text(value);
            this.slider.slider('value', value);
        },
        getValue: function() {
            return this.value;
        },
        getHandle: function() {
            return this.$el.find('a.ui-slider-handle');
        },
        getSlider: function() {
            return this.slider;
        },
        getSliderEl: function() {
            return this.$el;
        },
        next: function(callback) {
            if(this.value < this.total) {
                this.setValue(++this.value);
                if(callback) {
                    callback.call(this, this.value);
                }
            }
        },
        previous: function(callback) {
            if(this.value > 1) {
                this.setValue(--this.value);
                if(callback) {
                    callback.call(this, this.value);
                }
            }
        }
    };

    $.Pagination = function(options, element) {
        this.$el = $(element);
        this._init(options);
    };

    // the options
    $.Pagination.defaults = {
        value: 1,
        total: 5,
        width: 200,
        onChange: function(value) { return false; },
        onSlide: function(value) { return false; }
    };

    $.Pagination.prototype = {
        _init : function( options ) {
            // options
            this.options = $.extend(true, {}, $.Pagination.defaults, options);
            var transEndEventNames = {
                'WebkitTransition': 'webkitTransitionEnd',
                'MozTransition': 'transitionend',
                'OTransition': 'oTransitionEnd',
                'msTransition': 'MSTransitionEnd',
                'transition': 'transitionend'
            };
            this.transEndEventName = transEndEventNames[Modernizr.prefixed('transition')];
            $.fn.applyStyle = Modernizr.csstransitions ? $.fn.css : $.fn.animate;
            this._layout();
            this._initEvents();
        },
        _layout: function() {
            // next and previous
            this.$navNext = this.$el.find('nav > a.sp-next');
            this.$navPrev = this.$el.find('nav > a.sp-prev');
            // slider
            var $slider = $('<div class="sp-slider"></div>').appendTo(this.$el);
            this.slider = new $.Slider({value: this.options.value, total: this.options.total, width: this.options.width }, $slider);
            // control if the slider is opened/closed
            this.isSliderOpened = false;
        },
        _initEvents: function() {
            var self = this;

            this.slider.getHandle().on('click', function() {
                if(self.isSliderOpened) {
                    return false;
                }
                self.isSliderOpened = true;
                self.slider.getSliderEl().addClass('sp-slider-open');
                // expand slider wrapper
                self.$el.stop().applyStyle({width : self.options.width}, $.extend(true, [], {duration: '150ms'}));
                // hide navigation
                self.toggleNavigation(false);
                return false;
            });

            this.slider.getSlider().on({
                'slidestop': function(event, ui) {
                    if(!self.isSliderOpened) {
                        return false;
                    }

                    var animcomplete = function() {
                        self.isSliderOpened = false;
                        self.slider.getSliderEl().removeClass('sp-slider-open');
                        // show navigation
                        self.toggleNavigation(true);
                    };
                    self.$el.stop().applyStyle({width: 0}, $.extend(true, [], {duration: '150ms', complete: animcomplete })).on(self.transEndEventName, function() {
                        $( this ).off(self.transEndEventName);
                        animcomplete.call();
                    });

                    self.options.onChange(ui.value);
                },
                'slide': function(event, ui) {
                    if(!self.isSliderOpened) {
                        return false;
                    }
                    self.slider.setValue(ui.value);
                    self.options.onSlide(ui.value);
                }
            } );

            this.$navNext.on('click', function() {
                self.slider.next(function(value) {
                    self.options.onChange(value);
                });
                return false;
            });
            this.$navPrev.on('click', function() {
                self.slider.previous(function(value) {
                    self.options.onChange(value);
                });
                return false;
            });
        },
        toggleNavigation: function(toggle) {
            $.fn.render = toggle ? $.fn.show : $.fn.hide;
            this.$navNext.render();
            this.$navPrev.render();
        }
    }

    $.fn.pagination = function(options) {
        var instance = $.data(this, 'pagination');
        if (typeof options === 'string') {
            var args = Array.prototype.slice.call(arguments, 1);
            this.each(function() {
                instance[options].apply(instance, args);
            });
        } else {
            this.each(function() {
                instance ? instance._init() : instance = $.data(this, 'pagination', new $.Pagination(options, this));
            });
        }
        return instance;
    };
} )(jQuery, window);
