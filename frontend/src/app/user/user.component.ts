import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  mixedditForm: FormGroup;
  mixedditValue: any = {'': ''};

  constructor(private fb: FormBuilder) {
    this.createForm();
  }

  ngOnInit() {}

  onSubmit() {
    console.log(this.mixedditForm.value);
    this.mixedditValue = this.mixedditForm.value;
  }

  createForm() {
    this.mixedditForm = this.fb.group({
      subreddit: ['', Validators.required],
      playlist: ['', Validators.required]
    });
  }
}
