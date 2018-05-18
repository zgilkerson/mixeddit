import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss']
})
export class FaqComponent implements OnInit, AfterViewInit {
  private fragment: string;
  _sub;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this._sub = this.route.fragment.subscribe((hash: string) => {
      if (hash) {
        const cmp = document.getElementById(hash);
        if (cmp) {
          cmp.scrollIntoView();
        }
      } else {
        window.scrollTo(0, 0);
      }
    });
  }
  
  // ngAfterViewInit() {
  //   try {
  //     document.querySelector('#' + this.fragment).scrollIntoView();
  //   } catch (e) { }
  // }
}
