import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { SpotifyService } from '../spotify.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css'],
  providers: [SpotifyService]
})
export class UserComponent implements OnInit {
  mixedditForm: FormGroup;
  mixedditValue: any = {'': ''};

  constructor(private fb: FormBuilder, private spotify: SpotifyService) {
    this.createForm();
  }

  ngOnInit() {}

  onSubmit() {
    console.log(this.mixedditForm.value);
    this.spotify.putPlaylistReplace(this.mixedditForm.value).subscribe(
      (data) => this.mixedditValue = data,
      (error: HttpErrorResponse) => this.mixedditValue = error
    );
  }

  createForm() {
    this.mixedditForm = this.fb.group({
      subreddit: ['', Validators.required],
      playlist: ['', Validators.required]
    });
  }
}
